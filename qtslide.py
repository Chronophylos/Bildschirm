from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel, QMainWindow, QStatusBar

from config import Config


class Slideshow(QMainWindow):
    def __init__(self, _config: Config):
        self.config = _config
        super().__init__()

        if self.config.slideshow.fullscreen:
            self.showFullScreen()

        if self.config.slideshow.topmost:
            self.setWindowFlag(Qt.WindowStaysOnTopHint)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self.slide = QLabel()
        self.slide.show()

    def setFrame(self, frame):
        pixmap = QPixmap.fromImage(frame)
        self.slide.setPixmap(pixmap)

    def setImage(self, image_path):
        self.image = QImage(image_path)

    def start(self):
        self.setImage(r"D:\Work\Wallpaper\__alien_raiders_by_bluefley-d97mc82.jpg")
