const { contextBridge, ipcRenderer } = require('electron');
const { spawn, execFile } = require('child_process');
const path = require('path');

let pythonProcess = null;

contextBridge.exposeInMainWorld("api", {

  // ---------- NAV ----------
  navigate: (page) => ipcRenderer.send("navigate", page),
  exit: () => ipcRenderer.send("exit"),

  // ---------- OPEN YOUTUBE (DEBUG CHROME) ----------
  openYT: () => {

    const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
    const debugDir = "C:\\chrome-debug";

    execFile(
      chromePath,
      [
        "--remote-debugging-port=9222",
        `--user-data-dir=${debugDir}`,
        "https://youtube.com"
      ]
    );

  },

  // ---------- START CAMERA (SMART VERSION) ----------
  startCamera: () => {

    if (pythonProcess) return;

    const chromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe";
    const debugDir = "C:\\chrome-debug";
    const projectRoot = path.join(__dirname, "..");

    // 1️⃣ ensure debug Chrome + YouTube running
    execFile(
      chromePath,
      [
        "--remote-debugging-port=9222",
        `--user-data-dir=${debugDir}`,
        "https://youtube.com"
      ]
    );

    // 2️⃣ wait for Chrome startup before launching Python
    setTimeout(() => {

      pythonProcess = spawn(
        "py",
        ["-3.11", "-X", "utf8", "-m", "gestures.controller"],
        {
          cwd: projectRoot,
          shell: false
        }
      );

      pythonProcess.stdout.on("data", (data) => {
        const msg = data.toString().trim();
        ipcRenderer.send("gesture-status", msg);
      });

      pythonProcess.stderr.on("data", (data) => {

        const msg = data.toString();

        // ignore mediapipe / tensorflow / protobuf spam
        if (
          msg.includes("inference_feedback_manager") ||
          msg.includes("TensorFlow Lite") ||
          msg.includes("Feedback manager requires") ||
          msg.includes("SymbolDatabase.GetPrototype")
        ) return;

        ipcRenderer.send("gesture-status", "Error: " + msg.trim());
      });

      pythonProcess.on("close", () => {
        pythonProcess = null;
        ipcRenderer.send("gesture-status", "camera stopped");
      });

    }, 1500); // wait 1.5s for Chrome

  },

  // ---------- STOP CAMERA ----------
  stopCamera: () => {

    if (!pythonProcess) return;

    try {
      pythonProcess.kill("SIGTERM");
    } catch (e) {}

    pythonProcess = null;
    ipcRenderer.send("gesture-status", "camera stopped");
  }

});


// ---------- RECEIVE STATUS IN RENDERER ----------
ipcRenderer.on("gesture-status", (e, msg) => {
  window.dispatchEvent(new CustomEvent("gesture", { detail: msg }));
});