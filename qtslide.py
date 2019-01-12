from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QAction, QLabel, QMainWindow
from PIL import ImageQt, Image
import PIL

from config import Config
from logger import create_logger
from util import History, RandomImageList, get_files, getExif

logger = create_logger(__name__)


class Slideshow(QMainWindow):
    image_path = str()
    timer = QTimer()

    def __init__(self, app, _config: Config):
        self.app = app
        self.config = _config

        self.history = History(maxlen=self.config.slideshow.history_length)

        logger.debug("Creating Window")
        super().__init__()

        logger.debug("Creating Slide QLabel")
        self.slide = QLabel()

        logger.debug("Setting Slide Alignment to Center")
        self.slide.setAlignment(Qt.AlignCenter)

        logger.debug("Set Slide Background Color to black")
        self.slide.setStyleSheet("background-color: black;")

        logger.info("Setting Fullscreen to " +
                    str(self.config.slideshow.fullscreen))
        if self.config.slideshow.fullscreen:
            self.slide.setWindowState(Qt.WindowFullScreen)

        logger.debug("Ignoring Topmost")

        self.slide.show()

        logger.debug("Setting up Slideshow Timer")
        self.timer.timeout.connect(self.tick)

        logger.debug("Setting Actions")

        logger.debug("Creating Previous Image Action")
        prev_image_action = QAction("Previous Image", self)
        prev_image_action.triggered.connect(self.on_left)
        prev_image_action.setShortcut(Qt.Key_Left)
        self.slide.addAction(prev_image_action)

        logger.debug("Creating Next Image Action")
        next_image_action = QAction("Next Image", self)
        next_image_action.triggered.connect(self.on_right)
        next_image_action.setShortcut(Qt.Key_Right)
        self.slide.addAction(next_image_action)

        logger.debug("Creating Quit Action")
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit)
        quit_action.setShortcuts([Qt.Key_Q, Qt.Key_Escape])
        self.slide.addAction(quit_action)

    def on_left(self):
        logger.debug("Left Key Pressed")
        self.prevImage()

    def on_right(self):
        logger.debug("Right Key Pressed")
        self.nextImage()

    def resetTimer(self):
        logger.debug("Resetting Timer")
        self.timer.setInterval(self.config.slideshow.interval * 1000)

    def tick(self):
        logger.debug("Timer Tick Received")
        self.nextImage()

    def prevImage(self):
        self.resetTimer()
        logger.debug("Trying to get previous Image")
        if self.history.hasPrev():
            logger.info("Loading previous Image from History "
                        "[{}/{}]".format(self.history.cursor,
                                         self.history.size()))
            self.setImage(self.history.prev())
        else:
            logger.info("Cannot get previous Image. "
                        "Already at oldest available Image")

    def nextImage(self):
        self.resetTimer()
        logger.debug("Trying to get next Image")
        if self.history.hasNext():
            logger.info("Loading next Image from History")
            try:
                image = self.history.next()
            except IndexError as e:
                logger.exception(e)
                return self.quit(127)
            logger.debug("History Pointer Position: " +
                         str(self.history.cursor))
            self.setImage(image)
        else:
            logger.info("Loading Image from List")
            image = self.image_list.next()
            self.history.push(image)
            self.setImage(image)

    def quit(self, code=0):
        logger.info("Quitting")
        self.app.exit(code)

    def setImage(self, image_path):
        if self.image_path == image_path:
            logger.warn("Image already set. Skipping.")
            return

        logger.debug("Setting new Image")
        self.image_path = image_path

        logger.debug("Loading Image from " + str(image_path))
        image = ImageQt.ImageQt(Image.open(self.image_path))

        logger.debug("Image Type: " + str(type(Image)))
        logger.debug("Image Format: " + str(Image.format))

        if isinstance(image, PIL.Jpeg2KImagePlugin.Jpeg2KImageFile) or \
           isinstance(image, PIL.JpegImagePlugin.JpegImageFile):
            logger.debug("Getting EXIF Data from image")
            exif = getExif(image)

            logger.debug("Image EXIF: " + exif)

            if exif and "Orientation" in exif:
                logger.debug("Found Orientation in EXIF")
                pixmap = self.applyExifOrientation(image, exif)

        pixmap = QPixmap.fromImage(image)

        logger.debug("Scaling Image to fit " +
                     str(self.config.screen.width) + "x" +
                     str(self.config.screen.height) +
                     " while keeping Aspect Ratio")
        pixmap = pixmap.scaled(self.config.screen.width,
                               self.config.screen.height,
                               Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)

        logger.debug("Setting Slide Pixmap")
        self.slide.setPixmap(pixmap)

    def applyExifOrientation(self, image, exif):
        o = exif["Orientation"]
        if o == 1:
            pass
        elif o == 2:
            logger.debug("Mirroring Image horizontally")
            # mirror horizontal
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        elif o == 3:
            logger.debug("Rotating Image by 180 degree")
            # rotate 180 degree
            image = image.transpose(Image.ROTATE_180)
        elif o == 4:
            logger.debug("Mirroring Image vertically")
            # mirror vertical
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
        elif o == 5:
            logger.debug("Mirroring Image horizontally and "
                         "rotating by 270 degree")
            # mirror horizontal
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            # rotate 270 degree
            image = image.transpose(Image.ROTATE_270)
        elif o == 6:
            logger.debug("Rotating Image by 270 degree")
            # rotate 270 degree
            image = image.transpose(Image.ROTATE_270)
        elif o == 7:
            logger.debug("Mirroring Image horizontally and "
                         "rotating by 90 degree")
            # mirror horizontal
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
            # rotate 90 degree
            image = image.transpose(Image.ROTATE_90)
        elif o == 8:
            logger.debug("Rotating Image by 90 degree")
            # rotate 90 degree
            image = image.transpose(Image.ROTATE_90)
        else:
            logger.error("Unknown Orientation")
        return image

    def populateImageList(self):
        files = get_files(self.config.screen.image_path,
                          self.config.screen.file_types)
        if not files or len(files) == 0:
            logger.error("Image List is empty")
            return self.quit()
        self.image_list = RandomImageList(files)

    def start(self):
        logger.info("Populating Image List")
        self.populateImageList()
        self.nextImage()
        logger.info("Starting Slideshow")
        self.timer.start(self.config.slideshow.interval * 1000)
