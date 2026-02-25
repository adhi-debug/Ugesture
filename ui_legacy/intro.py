from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import QUrl, pyqtSignal

class IntroWindow(QWidget):
    video_finished = pyqtSignal()

    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle("Intro")

        layout = QVBoxLayout(self)

        # Video widget
        self.video_widget = QVideoWidget()
        layout.addWidget(self.video_widget)

        # Media player (plays video + audio)
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(self.video_widget)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))

        # Emit when video ends
        self.player.mediaStatusChanged.connect(self.check_status)

        # Auto resize to video resolution
        self.player.videoAvailableChanged.connect(self.resize_to_video)

        # Start
        self.player.play()

    def resize_to_video(self, available):
        if available:
            size = self.player.metaData("Resolution")
            if size:
                self.resize(size.width(), size.height())

    def check_status(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.video_finished.emit()
