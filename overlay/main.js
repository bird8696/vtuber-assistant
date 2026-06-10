const { app, BrowserWindow, screen, globalShortcut } = require("electron");
const path = require("path");
const express = require("express");

let bubbleWin;

function createWindows() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  bubbleWin = new BrowserWindow({
    width: 320,
    height: 420,
    x: 30,
    y: 30,
    transparent: true,
    frame: false,
    alwaysOnTop: true,
    resizable: true,
    skipTaskbar: true,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: false,
    },
  });
  bubbleWin.loadFile("bubble.html");
  bubbleWin.setAlwaysOnTop(true, "screen-saver");

  setInterval(() => {
    if (bubbleWin && !bubbleWin.isDestroyed())
      bubbleWin.setAlwaysOnTop(true, "screen-saver");
  }, 1000);
}

app.whenReady().then(() => {
  createWindows();

  // Ctrl+o 로 채팅창 토글
  globalShortcut.register("CommandOrControl+O", () => {
    if (bubbleWin) {
      if (bubbleWin.isVisible()) {
        bubbleWin.hide();
      } else {
        bubbleWin.show();
        bubbleWin.setAlwaysOnTop(true, "screen-saver");
      }
    }
  });
});

app.on("will-quit", () => {
  globalShortcut.unregisterAll();
});

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

const controlApp = express();
controlApp.use(express.json());

controlApp.post("/hide", (req, res) => {
  if (bubbleWin) bubbleWin.hide();
  res.json({ ok: true });
});

controlApp.post("/show", (req, res) => {
  if (bubbleWin) bubbleWin.show();
  res.json({ ok: true });
});

controlApp.listen(8766, "localhost");
