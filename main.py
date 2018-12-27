from config import Config
import toml
import sys

from logger import create_logger
logger = create_logger("main")


def main():
    with open("bildschirm.log", "w") as log:
        log.write("\n\n")

    try:
        logger.info("Loading Config")
        config = Config(toml.load("config.toml"))
    except toml.TomlDecodeError as e:
        logger.error("While Loading Config: " + e)
        return

    logger.info("Using {} as GUI".format(config.screen.gui))

    if config.screen.gui == "Qt":
        logger.debug("Importing required packages for Qt")
        from PyQt5.QtWidgets import QApplication
        from qtslide import Slideshow

        logger.debug("Creating QApplication")
        app = QApplication(sys.argv)

        logger.debug("Creating QtSlideshow")
        slideshow = Slideshow(app, config)
        slideshow.start()

        code = app.exec_()
        logger.info("Exiting with " + str(code))
        sys.exit(code)
    elif config.screen.gui == "Tk":
        logger.debug("Importing required packages for Tk")
        from tkslide import Slideshow

        logger.debug("Creating TkSlideshow")
        slideshow = Slideshow(config)
        slideshow.start()
        logger.info("Exiting")
    else:
        logger.error("Invalid GUI Type: " + config.screen.gui + " screen.gui should be one of Qt, Tk")


if __name__ == "__main__":
    main()
