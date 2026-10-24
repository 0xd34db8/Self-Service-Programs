# Self-Service Programs

A personal swiss-army knife repo filled with useful utilities, widgets & scripts

---

## 📑 Repository Catalog

### ⌨️ AutoHotkey Scripts (`AHK2_Scripts/`)

Scripts for Windows automation, keyboard remapping, and productivity enhancers.

- **[`Aggregate.ahk`](./AHK2_Scripts/Aggregate.ahk)** — Consolidated startup script combining the Copilot-to-Ctrl remap with fast Wi-Fi connection hotkeys (`Ctrl+Alt+H` for VITBPL, `Ctrl+Alt+V` for your own hotspot (update with your hostname) ). Features a master toggle (<kbd>`</kbd> / backtick).
- **[`copilot_to_ctrl_remap.ahk`](./AHK2_Scripts/copilot_to_ctrl_remap.ahk)** — Standalone script converting the Windows Copilot key (`Win+Shift+F23`) into a clean `Right Ctrl` press without modifier leakage.
- **[`Universal-Text-Editor.ahk`](./AHK2_Scripts/Universal-Text-Editor.ahk)** — AI-assisted text editor hotkey (`Ctrl+Alt+A`). Sends highlighted text to Google's Gemini API (`gemini-2.5-flash`) for rewriting, formatting, or instruction fulfillment and replaces it directly in place.
- **[`vs_code_shortcuts.ahk`](./AHK2_Scripts/vs_code_shortcuts.ahk)** — Replicates common VS Code text editing shortcuts system-wide (AHK v1.x). Automatically disables itself when VS Code is the active window.

> **Tip (Auto-start on Boot):** Press <kbd>Win</kbd> + <kbd>R</kbd>, enter `shell:startup`, and place a shortcut to your `.ahk` script into that folder.

---

### 🎨 Customizations (`Customizations/`)

Desktop themes, cursor packs, and browser styling.

- **[`codeforces_custom_styles.user.css`](./Customizations/codeforces_custom_styles.user.css)** — A modern SaaS-inspired UserStyle for Codeforces with flattened layouts, warm accents, and clean card aesthetics (install via Stylus).
- **Cursors:**
  - **[`Blue_Archive`](./Customizations/Cursors/Blue_Archive/)** — Custom Blue Archive cursor set with animated busy/loading pointers (`Install.inf`).
  - **[`Overwatch Pointer`](./Customizations/Cursors/Overwatch%20Pointer/)** — Overwatch-themed futuristic cursor pack (`Install.inf`).
  - **[`VA5H One`](./Customizations/Cursors/VA5H%20One/)** — Minimalist Dark and Light cursor themes.

> **How to install cursors:** Open the respective folder, right-click `Install.inf`, select **Install**, and apply the scheme under Windows Mouse Properties.

---

### 📓 Obsidian Plugins (`Obsidian Plugins/`)

Custom lightweight plugins built for Obsidian vaults.

- **[`AnchorTag-Adder-Plugin`](./Obsidian%20Plugins/AnchorTag-Adder-Plugin/)** — Obsidian plugin to append unique HTML anchor tags to headers for deep linking.
- **[`BackLink-Replacer-Plugin`](./Obsidian%20Plugins/BackLink-Replacer-Plugin/)** — Obsidian plugin to automate finding and updating internal backlink references.

---

### 🛠️ Tools & Utilities (`Tools/`)

Standalone tools, scripts, browser bookmarklets, and cheat sheets.

- **[`Youtube Speed Control.md`](./Tools/Youtube%20Speed%20Control.md)** — A draggable, resizable HUD bookmarklet allowing granular playback speed adjustments (up to 16x) with numeric input and quick-jump buttons.
- **[`NPTEL_Quiz_Widget.html`](./Tools/NPTEL_Quiz_Widget.html)** — A standalone offline dark-themed quiz practice app with instant feedback, scoring, and question review.
- **[`Qr.py`](./Tools/Qr.py)** — Python utility using `qrcode` and `Pillow` to quickly generate and save QR code images from the terminal.
- **[`SpoofDPI_on_windows/`](./Tools/SpoofDPI_on_windows/)** — Windows launcher (`Start_spoofdpi.bat`) and terminator (`Stop_spoofdpi.bat`) scripts to run SpoofDPI for bypassing Deep Packet Inspection without a VPN.
- **[`guest_additions_3mb.md`](./Tools/guest_additions_3mb.md)** — Minimal bash instructions to install VirtualBox guest integration (`virtualbox-guest-x11`) on Ubuntu/Debian VMs without desktop bloat.
- **[`FileTree_wo_nodeModules.md`](./Tools/FileTree_wo_nodeModules.md)** — A recursive PowerShell function (`Show-Tree`) that displays directory trees while ignoring bulky folders like `node_modules` and virtual environments.
- **[`video-intro/`](./Tools/video-intro/)** — An Electron desktop application designed to display a custom login splash video override upon Windows boot.

---

## ⚙️ Requirements & Dependencies

| Tool / Category    | Prerequisites                                                                                         |
| :----------------- | :---------------------------------------------------------------------------------------------------- |
| **AutoHotkey**     | [AutoHotkey v2.0+](https://www.autohotkey.com/) (except `vs_code_shortcuts.ahk` which requires v1.1+) |
| **Python Scripts** | Python 3.8+, `pip install qrcode pillow`                                                              |
| **UserStyles**     | [Stylus Browser Extension](https://add0n.com/stylus.html)                                             |
| **Electron App**   | Node.js LTS, npm                                                                                      |
