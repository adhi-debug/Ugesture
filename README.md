# ✋ UGesture — Gesture Controlled YouTube Player

UGesture is a **desktop application** that lets you control YouTube using **hand gestures** via your webcam.

Built with:

* 🐍 Python (MediaPipe + OpenCV + Selenium)
* ⚡ Electron (Desktop UI)
* 🎨 Modern Glassmorphism UI

You can **play, pause, seek, mute, and change playback speed** — all without touching the keyboard.

---

## 🚀 Features

✅ Hand gesture detection using MediaPipe
✅ Control YouTube playback in Chrome
✅ Electron desktop interface
✅ Real-time gesture status indicator
✅ Animated UI with glassmorphism design
✅ Auto-start camera from app
✅ Works with Chrome remote debugging

---

## 🖐 Supported Gestures

| Gesture           | Action                |
| ----------------- | --------------------- |
| Pinch fingers     | Play / Pause          |
| Wave Right        | Forward 5s            |
| Wave Left         | Backward 5s           |
| Two fingers up    | Mute                  |
| One finger up     | Unmute                |
| Move hand up/down | Change playback speed |

---

## 🏗 Project Structure

```
ugesture/
│
├── gestures/              # Python gesture engine
│   ├── controller.py
│   ├── detector.py
│   ├── recognizer.py
│   ├── actions.py
│   └── utils.py
│
├── electron/              # Electron desktop app
│   ├── main.js
│   ├── preload.js
│   ├── intro.html
│   ├── splash.html
│   ├── dashboard.html
│   └── dashboard.css
│
├── assets/                # Icons, fonts, video, chromedriver
│
├── app.py                 # Python entry launcher
└── README.md
```

---

## 🧰 Requirements

### Install Python dependencies

Use **Python 3.11 recommended**

```
pip install mediapipe opencv-python selenium numpy protobuf
```

---

### Install Electron dependencies

Inside `/electron` folder:

```
npm install
```

---

## ▶️ How To Run

### 1️⃣ Start Chrome in debugging mode

Run:

```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\chrome-debug"
```

Then open YouTube in that Chrome.

---

### 2️⃣ Start the desktop app

Inside `/electron`:

```
npm start
```

---

### 3️⃣ Click inside app

* **Start Camera**
* **Open YouTube**

Control with gestures.

---

## 📦 Build Windows Installer

Inside `/electron`:

```
npm run build
```

Installer will appear in:

```
electron/dist/
```

---

## 🛠 Troubleshooting

### Camera not opening

* Ensure webcam permission allowed
* Close other apps using camera

### Chrome not detected

* Make sure Chrome launched with debugging port 9222

### Gesture lag

* Use good lighting
* Keep hand inside camera frame

---

## 🌟 Future Improvements

* Embed camera inside Electron UI
* Multi-tab YouTube control
* Custom gesture training
* Dark/light themes
* System tray integration

---

## 👨‍💻 Author

Built by **V . Chandanadhithyan**

If you like this project ⭐ star the repo!

---

## 📄 License

MIT License © 2026 **V Adhithyan**

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files to deal in the Software
without restriction, including without limitation the rights to use, copy,
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.
