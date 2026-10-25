#!/usr/bin/env python3
"""
Portable 1-Click APKS Patcher for MDickie 3D Universe Games
------------------------------------------------------------
Fully portable utility with zero hardcoded paths or system dependencies.
Automatically:
  1. Unpacks input .apks bundle
  2. Dynamically detects target package from AndroidManifest.xml
  3. Auto-discovers Store.huq, Characters.kn, and Application.OpenURL RVAs via signature scanning
  4. Surgically patches Store.huq, Characters.kn, and Application.OpenURL in libil2cpp.so
  5. Neutralizes PairIP Google Play Integrity and Licensing checks in classes2.dex
  6. Clones package identifiers across binary manifests and DEX string tables for dual-install
  7. Runs zipalign and v2/v3 signing using the local uber-apk-signer.jar
  8. Bundles the result into an output .apks in the same directory
"""

import os
import sys
import re
import shutil
import zlib
import hashlib
import zipfile
import struct
import subprocess
import argparse
import tempfile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Standard ARM64 bytecodes
ARM64_RET_TRUE = b'\x20\x00\x80\x52\xc0\x03\x5f\xd6'  # mov w0, #1; ret
ARM64_RET_VOID = b'\xc0\x03\x5f\xd6'                  # ret

# Known RVA database (optional fast-path; auto-discovery runs if missing)
KNOWN_TARGETS = {
    "com.MDickie.InfiniteLives": {
        "huq_rva": 0x16d97b0,
        "kn_rva": 0x16c4960,
        "openurl_rva": 0x3271098
    }
}

def scan_store_huq(so_bytes: bytes) -> int:
    """Auto-detects Store.huq subscription check via ARM64 machine code signature."""
    # Pattern: str x30, [sp, #-16]! ; cbz x1, ... ; ldr x8, [x1, #16] ; cbz x8, ... ; ldr x8, [x8, #16]
    pattern = re.compile(rb'\xfe\x0f\x1f\xf8.\x01\x00\xb4\x28\x08\x40\xf9.\x00\x00\xb4\x08\x09\x40\xf9', re.DOTALL)
    m = pattern.search(so_bytes)
    return (m.start() + 0x4000) if m else 0

def scan_characters_kn(so_bytes: bytes) -> int:
    """Auto-detects Characters.kn character unlock check via ARM64 machine code signature."""
    # Pattern: stp x29, x30, [sp, #-64]! ; stp x19, x20 ; stp x21, x22 ; stp x23, x24 ; adrp x19 ; adrp x20 ; ldrb w8
    pattern = re.compile(rb'\xfe\x67\xbc\xa9\xf8\x5f\x01\xa9\xf6\x57\x02\xa9\xf4\x4f\x03\xa9..\x01\xb0..\x01\xf0..\x7c\x39', re.DOTALL)
    m = pattern.search(so_bytes)
    return (m.start() + 0x4000) if m else 0

def scan_application_openurl(so_bytes: bytes) -> int:
    """Auto-detects UnityEngine.Application.OpenURL via ARM64 machine code signature."""
    # Pattern: sub sp, sp, #0x50 ; str x30, [sp, #24] ; stp x20, x19, [sp, #32] ; adrp x20 ; mov x19, x0 ; ldrb w8, [x20]
    pattern = re.compile(rb'\xff\x43\x01\xd1\xfe\x1b\x00\xf9\xf4\x4f\x04\xa9..\x00\xf0\xf3\x03\x00\xaa..\x74\x39\x88\x01\x00\x37', re.DOTALL)
    m = pattern.search(so_bytes)
    return (m.start() + 0x4000) if m else 0

def fix_dex_checksums(dex_bytes: bytearray) -> bytearray:
    """Recalculates SHA-1 signature and Adler32 checksum in DEX header."""
    sha1 = hashlib.sha1(dex_bytes[32:]).digest()
    dex_bytes[12:32] = sha1
    adler = zlib.adler32(dex_bytes[12:]) & 0xffffffff
    dex_bytes[8:12] = struct.pack('<I', adler)
    return dex_bytes

def clone_package_string(data: bytes, orig_pkg: str, new_pkg: str) -> bytes:
    """Replaces package occurrences preserving identical string length."""
    if len(orig_pkg) != len(new_pkg):
        raise ValueError(f"Clone package '{new_pkg}' must match length of '{orig_pkg}' ({len(orig_pkg)} chars)")
    
    out = data.replace(orig_pkg.encode('utf-8'), new_pkg.encode('utf-8'))
    out = out.replace(orig_pkg.encode('utf-16le'), new_pkg.encode('utf-16le'))
    return out

class PortablePatcher:
    def __init__(self, tools_dir: str = None):
        self.tools_dir = os.path.abspath(tools_dir or BASE_DIR)
        self.signer_jar = os.path.join(self.tools_dir, "uber-apk-signer.jar")
        self.keystore = os.path.join(self.tools_dir, "debug.keystore")

        if not os.path.exists(self.signer_jar):
            raise FileNotFoundError(f"Missing uber-apk-signer.jar in {self.tools_dir}")
        if not os.path.exists(self.keystore):
            raise FileNotFoundError(f"Missing debug.keystore in {self.tools_dir}")

    def patch_il2cpp_binary(self, so_bytes: bytearray, huq_rva: int, kn_rva: int, openurl_rva: int) -> bytearray:
        """Surgically patches ARM64 native functions."""
        e_phoff = struct.unpack_from('<Q', so_bytes, 32)[0]
        e_phentsize = struct.unpack_from('<H', so_bytes, 54)[0]
        e_phnum = struct.unpack_from('<H', so_bytes, 56)[0]

        segments = []
        for i in range(e_phnum):
            p = so_bytes[e_phoff + i * e_phentsize : e_phoff + (i + 1) * e_phentsize]
            p_type, _, p_offset, p_vaddr, _, p_filesz, _, _ = struct.unpack('<IIQQQQQQ', p[:56])
            if p_type == 1:
                segments.append((p_vaddr, p_offset, p_filesz))

        def rva_to_off(rva):
            for vaddr, offset, filesz in segments:
                if vaddr <= rva < vaddr + filesz:
                    return offset + (rva - vaddr)
            return rva - 0x4000

        if huq_rva > 0:
            off = rva_to_off(huq_rva)
            so_bytes[off : off + len(ARM64_RET_TRUE)] = ARM64_RET_TRUE
            print(f"  [+] Patched Store.huq at offset {hex(off)} (RVA {hex(huq_rva)}) -> mov w0, #1; ret")

        if kn_rva > 0:
            off = rva_to_off(kn_rva)
            so_bytes[off : off + len(ARM64_RET_TRUE)] = ARM64_RET_TRUE
            print(f"  [+] Patched Characters.kn at offset {hex(off)} (RVA {hex(kn_rva)}) -> mov w0, #1; ret")

        if openurl_rva > 0:
            off = rva_to_off(openurl_rva)
            so_bytes[off : off + len(ARM64_RET_VOID)] = ARM64_RET_VOID
            print(f"  [+] Patched Application.OpenURL at offset {hex(off)} (RVA {hex(openurl_rva)}) -> ret")

        return so_bytes

    def patch_dex_licensing(self, dex_bytes: bytearray) -> bytearray:
        """Neutralizes PairIP Google Play licensing check dispatchers."""
        # SignatureCheck.verifySignatureMatches
        sig_match = b'\x62\x00\x66\x0c'
        pos = dex_bytes.find(sig_match)
        if pos != -1:
            dex_bytes[pos:pos+4] = b'\x12\x10\x0f\x00'

        # SignatureCheck.verifyIntegrity
        sig_int = b'\x6e\x10'
        pos = dex_bytes.find(sig_int, pos if pos != -1 else 0)
        if pos != -1:
            dex_bytes[pos:pos+2] = b'\x0e\x00'

        # LicenseClient.isLocalCheckPassed
        local_chk = b'\x62\x00\xc2\x0c'
        pos = dex_bytes.find(local_chk)
        if pos != -1:
            dex_bytes[pos:pos+4] = b'\x12\x10\x0f\x00'

        # LicenseClient startErrorDialogActivity & startPaywallActivity
        target_acts = b'\x70\x10'
        pos = 0
        while True:
            pos = dex_bytes.find(target_acts, pos)
            if pos == -1: break
            if pos in [0x6795c, 0x67994]:
                dex_bytes[pos:pos+2] = b'\x0e\x00'
            pos += 2

        return fix_dex_checksums(dex_bytes)

    def process_apks(self, input_apks: str, output_apks: str, clone: bool = True,
                     huq_rva: int = None, kn_rva: int = None, openurl_rva: int = None):
        """Processes an input .apks bundle and generates an unlocked, signed .apks bundle."""
        input_apks = os.path.abspath(input_apks)
        output_apks = os.path.abspath(output_apks)

        print(f"[*] Processing package: {os.path.basename(input_apks)}")
        work_dir = tempfile.mkdtemp(prefix="mdickie_portable_")
        unpacked_dir = os.path.join(work_dir, "unpacked")
        to_sign_dir = os.path.join(work_dir, "to_sign")
        signed_dir = os.path.join(work_dir, "signed")

        os.makedirs(unpacked_dir, exist_ok=True)
        os.makedirs(to_sign_dir, exist_ok=True)

        try:
            with zipfile.ZipFile(input_apks, 'r') as z:
                z.extractall(unpacked_dir)

            apk_files = [f for f in os.listdir(unpacked_dir) if f.endswith('.apk')]
            base_apk_name = next((f for f in apk_files if 'base' in f.lower()), None)

            if not base_apk_name:
                raise FileNotFoundError("base.apk not found inside the .apks archive.")

            # Dynamically detect package name from base.apk AndroidManifest.xml
            base_path = os.path.join(unpacked_dir, base_apk_name)
            with zipfile.ZipFile(base_path, 'r') as zbase:
                manifest_data = zbase.read('AndroidManifest.xml')

            pkg_match = re.search(rb'com\.MDickie\.[a-zA-Z0-9_]+', manifest_data)
            if pkg_match:
                orig_pkg = pkg_match.group(0).decode('ascii')
            else:
                orig_pkg = "com.MDickie.InfiniteLives"

            # Create dual-install package name of identical length
            last_char = orig_pkg[-1]
            new_char = 'z' if last_char.lower() != 'z' else 'x'
            new_pkg = orig_pkg[:-1] + new_char if clone else orig_pkg

            target_cfg = KNOWN_TARGETS.get(orig_pkg, {})
            huq = huq_rva if huq_rva is not None else target_cfg.get("huq_rva", None)
            kn = kn_rva if kn_rva is not None else target_cfg.get("kn_rva", None)
            openurl = openurl_rva if openurl_rva is not None else target_cfg.get("openurl_rva", None)

            print(f"[*] Detected Package: {orig_pkg}")
            print(f"[*] Dual-Install Package: {new_pkg} (Cloning: {clone})")

            for apk_name in apk_files:
                src_apk = os.path.join(unpacked_dir, apk_name)
                dst_apk = os.path.join(to_sign_dir, apk_name)
                print(f"[*] Patching split: {apk_name}...")

                with zipfile.ZipFile(src_apk, 'r') as zin, zipfile.ZipFile(dst_apk, 'w') as zout:
                    for item in zin.infolist():
                        if item.filename.startswith('META-INF/') and any(item.filename.endswith(ext) for ext in ['.SF', '.RSA', '.DSA', '.MF', '.EC']):
                            continue

                        data = zin.read(item.filename)

                        if item.filename == 'lib/arm64-v8a/libil2cpp.so':
                            print("  [+] Analyzing libil2cpp.so with dynamic signature scanning...")
                            # Run dynamic signature scanner if RVAs not provided or known
                            final_huq = huq or scan_store_huq(data)
                            final_kn = kn or scan_characters_kn(data)
                            final_openurl = openurl or scan_application_openurl(data)

                            print(f"  [+] Target RVAs: huq={hex(final_huq)}, kn={hex(final_kn)}, openurl={hex(final_openurl)}")
                            data = self.patch_il2cpp_binary(bytearray(data), final_huq, final_kn, final_openurl)

                        elif item.filename == 'classes2.dex':
                            print("  [+] Neutralizing classes2.dex licensing checks...")
                            data = self.patch_dex_licensing(bytearray(data))
                            if clone:
                                data = clone_package_string(data, orig_pkg, new_pkg)
                                data = fix_dex_checksums(bytearray(data))

                        elif clone:
                            if item.filename == 'AndroidManifest.xml' or item.filename.endswith('.dex'):
                                data = clone_package_string(data, orig_pkg, new_pkg)
                                if item.filename.endswith('.dex'):
                                    data = fix_dex_checksums(bytearray(data))

                        zout.writestr(item, data)

            print("[*] Running uber-apk-signer for zipalign and v2/v3 signatures...")
            cmd = [
                "java", "-jar", self.signer_jar,
                "-a", to_sign_dir,
                "--ks", self.keystore,
                "--ksAlias", "androiddebugkey",
                "--ksPass", "android",
                "--ksKeyPass", "android",
                "-o", signed_dir
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                raise RuntimeError(f"Signing failed: {res.stderr}")
            print("  [+] Splits successfully signed and aligned [v2/v3 verified]")

            print(f"[*] Assembling final .apks package: {output_apks}")
            os.makedirs(os.path.dirname(output_apks), exist_ok=True)
            with zipfile.ZipFile(output_apks, 'w', compression=zipfile.ZIP_STORED) as zout:
                for f in os.listdir(signed_dir):
                    if f.endswith('-aligned-signed.apk'):
                        clean_name = f.replace('-aligned-signed.apk', '.apk')
                        zout.write(os.path.join(signed_dir, f), clean_name)
                        print(f"  [+] Included: {clean_name}")

            size_mb = round(os.path.getsize(output_apks) / (1024 * 1024), 2)
            print(f"[+] Complete! Output written to {output_apks} ({size_mb} MB)")

        finally:
            shutil.rmtree(work_dir, ignore_errors=True)

def main():
    parser = argparse.ArgumentParser(description="Universal 1-Click APKS Patcher for MDickie 3D Universe")
    parser.add_argument("input_apks", help="Path to input .apks file")
    parser.add_argument("-o", "--output", required=True, help="Path to output .apks file")
    parser.add_argument("--no-clone", action="store_true", help="Do not rename package identifier (disables dual-install)")
    parser.add_argument("--tools-dir", default=None, help="Directory containing uber-apk-signer.jar and debug.keystore")
    parser.add_argument("--huq-rva", type=lambda x: int(x, 0), default=None, help="Custom RVA override for Store.huq")
    parser.add_argument("--kn-rva", type=lambda x: int(x, 0), default=None, help="Custom RVA override for Characters.kn")
    parser.add_argument("--openurl-rva", type=lambda x: int(x, 0), default=None, help="Custom RVA override for Application.OpenURL")

    args = parser.parse_args()
    patcher = PortablePatcher(args.tools_dir)
    patcher.process_apks(
        input_apks=args.input_apks,
        output_apks=args.output,
        clone=not args.no_clone,
        huq_rva=args.huq_rva,
        kn_rva=args.kn_rva,
        openurl_rva=args.openurl_rva
    )

if __name__ == "__main__":
    main()
