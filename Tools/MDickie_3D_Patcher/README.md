# MDickie 3D Universe — Portable 1-Click Patcher

A completely self-contained, portable tool for unlocking the built-in character editor and eliminating store redirect loops on MDickie 3D Android games (*Infinite Lives*, *Wrestling Empire*, *Old School*, *Hard Time III*, *Extra Lives 3D*).

---

## Quick Start (1-Click)

1. Drop your original game **`.apks`** file into this folder.
2. Double-click **`run_patcher.bat`**.
3. Your new **`[game]-unlocked.apks`** file will appear right in the same folder.
4. Install it on your Android device (using SAI or ADB). It installs **directly alongside** the original game.

---

## Contents of This Directory

* **`run_patcher.bat`**: Automatic 1-click launcher for Windows.
* **`patcher.py`**: Portable Python engine (pure Python standard library, zero pip packages).
* **`uber-apk-signer.jar`**: Standalone JAR for zipalign and official v2/v3 APK signing.
* **`debug.keystore`**: Android debug keystore for certificate generation.

---

## Advanced CLI Usage

```bash
# Standard 1-click run (auto-discovers all RVAs via signature scanning)
python patcher.py "InfiniteLives-1.0.8.apks" -o "InfiniteLives-Unlocked.apks"

# Disable dual-install (replace original app instead of installing alongside)
python patcher.py "InfiniteLives-1.0.8.apks" -o "InfiniteLives-Unlocked.apks" --no-clone

# (Optional) Explicit RVA overrides if needed
python patcher.py "Game.apks" \
    --huq-rva 0x... \
    --kn-rva 0x... \
    --openurl-rva 0x... \
    -o "Game-Unlocked.apks"
```
