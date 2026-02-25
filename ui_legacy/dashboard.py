import sys
import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QPushButton, QGraphicsDropShadowEffect, QFrame
)
from PyQt5.QtGui import QPixmap, QFont, QCursor, QColor
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation

from gestures.actions import GestureActions
from gestures.utils import resource_path



class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ugesture Dashboard")
        self.setGeometry(200, 100, 960, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Gesture actions instance
        self.actions = GestureActions()
        self.camera_process = None

        # Main container
        central_widget = QWidget()
        central_widget.setObjectName("central")
        self.setCentralWidget(central_widget)

        # Glassmorphism background (charcoal/dark gray gradient with opacity)
        self.setStyleSheet("""
            #central {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(30,30,30,220),
                                            stop:1 rgba(50,50,50,220));
                border-radius: 20px;
            }
            QLabel {
                color: white;
            }
        """)

        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        # Header
        self.header = QLabel("U g e s t u r e    D a s h b o a r d")
        self.header.setAlignment(Qt.AlignCenter)
        self.header.setFont(QFont("Floe", 55))
        layout.addWidget(self.header)

        # Divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("color: rgba(255,255,255,50);")
        layout.addWidget(divider)

        # Gesture buttons container
        grid = QHBoxLayout()
        grid.setSpacing(30)
        layout.addLayout(grid)

        # Add gesture action cards
        self.add_action_card(grid, "Play / Pause", resource_path("assets/icons/play.png"), "play_pause")
        self.add_action_card(grid, "Speed Up", resource_path("assets/icons/speedup.png"), "speed_up")
        self.add_action_card(grid, "Speed Down", resource_path("assets/icons/slow.png"), "speed_down")
        self.add_action_card(grid, "Forward", resource_path("assets/icons/forward.png"), "forward")
        self.add_action_card(grid, "Backward", resource_path("assets/icons/backward.png"), "backward")
        self.add_action_card(grid, "Mute", resource_path("assets/icons/mute.png"), "mute")
        self.add_action_card(grid, "Unmute", resource_path("assets/icons/unmute.png"), "unmute")

        # Status label
        self.status_label = QLabel("🟢 Ready for gestures...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Etude Noire Regular", 20))
        layout.addWidget(self.status_label)

        # Camera toggle button
        self.camera_btn = QPushButton("🎥 Start Camera Control")
        self.camera_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.camera_btn.setFixedHeight(55)
        self.camera_btn.setFont(QFont("Moderniz", 14))
        layout.addWidget(self.camera_btn)
        self.setup_camera_button()

        # Footer Exit button
        footer = QHBoxLayout()
        footer.addStretch()
        exit_btn = QPushButton("Exit")
        exit_btn.setCursor(QCursor(Qt.PointingHandCursor))
        exit_btn.setFixedHeight(55)
        exit_btn.setFixedWidth(80)
        exit_btn.clicked.connect(self.close)
        exit_btn.setFont(QFont("Moderniz", 11))
        self.setup_exit_button(exit_btn)
        footer.addWidget(exit_btn)
        layout.addLayout(footer)

    # ---------- Gesture Card ----------
    def add_action_card(self, layout, title, icon_path, action_name):
        card = QPushButton()
        card.setCursor(QCursor(Qt.PointingHandCursor))
        card.setFixedSize(140, 160)
        card.original_y = None  # store original y position later

        # Glass-like card style
        card.setStyleSheet("""
            QPushButton {
                background: rgba(0,200,255,30);
                border-radius: 18px;
                border: 1px solid rgba(0,200,255,50);
                color: white;
            }
            QPushButton:hover {
                color: black;
            }
        """)
        card.clicked.connect(lambda: self.actions.perform(action_name))

        # Glow effect
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(0)
        glow.setColor(QColor(0, 180, 255))
        glow.setOffset(0, 0)
        card.setGraphicsEffect(glow)

        # Hover lift + glow animation
        def on_enter(event):
            if card.original_y is None:
                card.original_y = card.y()  # store original Y only once

            blur_anim = QPropertyAnimation(glow, b"blurRadius")
            blur_anim.setDuration(200)
            blur_anim.setStartValue(0)
            blur_anim.setEndValue(25)
            blur_anim.start()
            card.glow_anim = blur_anim

            lift_anim = QPropertyAnimation(card, b"geometry")
            lift_anim.setDuration(200)
            lift_anim.setStartValue(card.geometry())
            lift_anim.setEndValue(QRect(card.x(), card.original_y - 8, card.width(), card.height()))
            lift_anim.start()
            card.lift_anim = lift_anim

        def on_leave(event):
            blur_anim = QPropertyAnimation(glow, b"blurRadius")
            blur_anim.setDuration(200)
            blur_anim.setStartValue(25)
            blur_anim.setEndValue(0)
            blur_anim.start()
            card.glow_anim = blur_anim

            drop_anim = QPropertyAnimation(card, b"geometry")
            drop_anim.setDuration(200)
            drop_anim.setStartValue(card.geometry())
            drop_anim.setEndValue(QRect(card.x(), card.original_y, card.width(), card.height()))
            drop_anim.start()
            card.lift_anim = drop_anim

        card.enterEvent = lambda event: on_enter(event)
        card.leaveEvent = lambda event: on_leave(event)

        # Icon + title
        vbox = QVBoxLayout(card)
        vbox.setAlignment(Qt.AlignCenter)
        icon_label = QLabel()
        pixmap = QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignCenter)
        text_label = QLabel(title)
        text_label.setFont(QFont("KotaSansDemo-Italic", 15))
        text_label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(icon_label)
        vbox.addSpacing(10)
        vbox.addWidget(text_label)

        layout.addWidget(card)

    # ---------- Camera Button ----------
    def setup_camera_button(self):
        # Glassmorphism gradient
        self.camera_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 rgba(0,255,255,30),
                                            stop:1 rgba(0,200,255,30));
                border-radius: 20px;
                border: 2px solid rgba(0,255,255,50);
                color: white;
            }
        """)
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(0)
        glow.setColor(QColor(0,200,255))
        glow.setOffset(0,0)
        self.camera_btn.setGraphicsEffect(glow)

        # Hover lift + glow
        def on_enter(event):
            blur_anim = QPropertyAnimation(glow, b"blurRadius")
            blur_anim.setDuration(200)
            blur_anim.setStartValue(0)
            blur_anim.setEndValue(25)
            blur_anim.start()
            self.camera_btn.glow_anim = blur_anim

            lift_anim = QPropertyAnimation(self.camera_btn, b"geometry")
            lift_anim.setDuration(200)
            lift_anim.setStartValue(self.camera_btn.geometry())
            lift_anim.setEndValue(QRect(self.camera_btn.x(), self.camera_btn.y() - 6,
                                        self.camera_btn.width(), self.camera_btn.height()))
            lift_anim.start()
            self.camera_btn.lift_anim = lift_anim

        def on_leave(event):
            blur_anim = QPropertyAnimation(glow, b"blurRadius")
            blur_anim.setDuration(200)
            blur_anim.setStartValue(25)
            blur_anim.setEndValue(0)
            blur_anim.start()
            self.camera_btn.glow_anim = blur_anim

            drop_anim = QPropertyAnimation(self.camera_btn, b"geometry")
            drop_anim.setDuration(200)
            drop_anim.setStartValue(self.camera_btn.geometry())
            drop_anim.setEndValue(QRect(self.camera_btn.x(), self.camera_btn.y() + 6,
                                        self.camera_btn.width(), self.camera_btn.height()))
            drop_anim.start()
            self.camera_btn.lift_anim = drop_anim

        self.camera_btn.enterEvent = lambda event: on_enter(event)
        self.camera_btn.leaveEvent = lambda event: on_leave(event)
        self.camera_btn.clicked.connect(self.toggle_camera)

    # ---------- Exit Button ----------
    def setup_exit_button(self, btn):
        btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                            stop:0 #ff4d4d, stop:1 #e60000);
                border-radius: 20px;
                border: 2px solid #ff6666;
                color: white;
                font-weight: bold;
            }
        """)
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(0)
        glow.setColor(QColor(255,80,80))
        glow.setOffset(0,0)
        btn.setGraphicsEffect(glow)

        def on_enter(event):
            blur_anim = QPropertyAnimation(glow, b"blurRadius")
            blur_anim.setDuration(200)
            blur_anim.setStartValue(0)
            blur_anim.setEndValue(20)
            blur_anim.start()
            btn.glow_anim = blur_anim

            lift_anim = QPropertyAnimation(btn, b"geometry")
            lift_anim.setDuration(200)
            lift_anim.setStartValue(btn.geometry())
            lift_anim.setEndValue(QRect(btn.x(), btn.y() - 6, btn.width(), btn.height()))
            lift_anim.start()
            btn.lift_anim = lift_anim

        def on_leave(event):
            blur_anim = QPropertyAnimation(glow, b"blurRadius")
            blur_anim.setDuration(200)
            blur_anim.setStartValue(20)
            blur_anim.setEndValue(0)
            blur_anim.start()
            btn.glow_anim = blur_anim

            drop_anim = QPropertyAnimation(btn, b"geometry")
            drop_anim.setDuration(200)
            drop_anim.setStartValue(btn.geometry())
            drop_anim.setEndValue(QRect(btn.x(), btn.y() + 6, btn.width(), btn.height()))
            drop_anim.start()
            btn.lift_anim = drop_anim

        btn.enterEvent = lambda event: on_enter(event)
        btn.leaveEvent = lambda event: on_leave(event)

    # ---------- Camera Control ----------
    def toggle_camera(self):
        if self.camera_process is None:
            self.camera_process = subprocess.Popen([sys.executable, "-m", "gestures.controller"])
            self.camera_btn.setText("⏹ Stop Camera Control")
        else:
            self.camera_process.terminate()
            self.camera_process = None
            self.camera_btn.setText("🎥 Start Camera Control")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Dashboard()
    win.show()
    sys.exit(app.exec_())
