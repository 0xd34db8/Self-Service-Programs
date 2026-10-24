const { app, BrowserWindow, ipcMain } = require("electron");

let win;

app.whenReady().then(() => {
  win = new BrowserWindow({
    fullscreen: true,
    frame: false,
    alwaysOnTop: true,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
    },
  });

  win.loadFile("index.html");

  win.on("closed", () => {
    if (!win) return;
    let opacity = 1.0;
    const fade = setInterval(() =>{
        opacity -=0.05;
        if(opacity<=0){
            clearInterval(fade);
            app.quit();
        }else {
            win.setOpacity(opacity);
        }
    }, 50)
  });
});

ipcMain.on("quit-app", () => {
  app.quit();
});

app.on("window-all-closed", () => {
  app.quit();
});
