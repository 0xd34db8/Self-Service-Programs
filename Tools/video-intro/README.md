An Electron app that overrides the default OS splash screen after login and replaces it with a custom video.

How to rebuild:

---

Prereqs:

Node.js (LTS recommended)

npm (comes with Node)

---

1️⃣ Build the Windows executable:

```bash
cd resources/app
npm install
npx electron-packager . video-intro --platform=win32 --arch=x64 --overwrite

```

2️⃣ Done.

It will generate a folder like:

video-intro-win32-x64/

Inside that folder:

video-intro.exe

That’s your executable.
