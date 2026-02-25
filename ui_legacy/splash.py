import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen, QGraphicsDropShadowEffect
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation
from gestures.utils import resource_path

class GlowSplash(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Start fully transparent for fade-in
        self.setWindowOpacity(0)

        # --- Glow effect ---
        glow = QGraphicsDropShadowEffect()
        glow.setBlurRadius(50)
        glow.setColor(QColor(0, 180, 255))  # cyan glow
        glow.setOffset(0, 0)
        self.setGraphicsEffect(glow)

        # --- Fade-in ---
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(2000)  # 2s fade-in
        self.fade_in.setStartValue(0)
        self.fade_in.setEndValue(1)
        self.fade_in.start()

class SplashScreen(GlowSplash):
    def __init__(self, pixmap_path, duration=3000):
        pixmap = QPixmap(pixmap_path).scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        super().__init__(pixmap)
        self.duration = duration

        # Auto close with fade-out
        QTimer.singleShot(self.duration, self.fade_out_and_close)

    def fade_out_and_close(self):
        # Fade out using windowOpacity to avoid deleted effect issue
        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setDuration(1000)
        self.fade_out.setStartValue(1)
        self.fade_out.setEndValue(0)
        self.fade_out.finished.connect(self.close)
        self.fade_out.start()

# Debug run
if __name__ == "__main__":
    app = QApplication(sys.argv)
    splash = SplashScreen(resource_path("assets/logo.png"), duration=3000)
    splash.show()
    sys.exit(app.exec_())
