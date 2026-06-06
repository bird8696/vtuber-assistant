const { app, BrowserWindow, screen } = require("electron");
const path = require("path");
const express = require("express");

let bubbleWin, modelWin;

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

  modelWin = new BrowserWindow({
    width: 560,
    height: 900,
    x: width - 580,
    y: height - 920,
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
  modelWin.loadFile("model.html");
  modelWin.setAlwaysOnTop(true, "screen-saver");
  // modelWin.webContents.openDevTools({ mode: "detach" });

  setInterval(() => {
    if (bubbleWin && !bubbleWin.isDestroyed())
      bubbleWin.setAlwaysOnTop(true, "screen-saver");
    if (modelWin && !modelWin.isDestroyed())
      modelWin.setAlwaysOnTop(true, "screen-saver");
  }, 1000);
}

app.whenReady().then(createWindows);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

const controlApp = express();
controlApp.use(express.json());

controlApp.post("/hide", (req, res) => {
  if (bubbleWin) bubbleWin.hide();
  if (modelWin) modelWin.hide();
  res.json({ ok: true });
});

controlApp.post("/show", (req, res) => {
  if (bubbleWin) bubbleWin.show();
  if (modelWin) modelWin.show();
  res.json({ ok: true });
});

controlApp.listen(8766, "localhost");
