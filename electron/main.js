const { app, BrowserWindow, ipcMain, Menu } = require('electron');
const path = require('path');

let win;

function createWindow(){

  win = new BrowserWindow({
    width:1100,
    height:700,

    // ⭐ keep native Windows buttons
    frame:true,

    // ⭐ allow minimize/maximize
    resizable:true,
    minimizable:true,
    maximizable:true,
    fullscreenable:true,

    backgroundColor:"#0a0c10",
    icon: path.join(__dirname, "../assets/icon.ico"),

    webPreferences:{
      preload: path.join(__dirname,"preload.js"),
      contextIsolation:true,
      nodeIntegration:false,
      sandbox:false
    }
  });

  // ⭐ REMOVE TOP MENU (File/Edit/View...)
  Menu.setApplicationMenu(null);

  win.loadFile("intro.html");
}

app.whenReady().then(createWindow);

ipcMain.on("navigate",(e,page)=>{
  if(win) win.loadFile(page);
});

ipcMain.on("exit",()=>{
  app.quit();
});

ipcMain.on("gesture-status",(e,msg)=>{
  if(win) win.webContents.send("gesture-status",msg);
});