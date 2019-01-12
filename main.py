from config import Config
import toml
import sys

from logger import create_logger
logger = create_logger("main")


def exception_hook(exctype, value, traceback):
    logger.error(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


def main():
    logger.debug("Setting Custom Excepthook")
    sys._excepthook = sys.excepthook
    sys.excepthook = exception_hook

    logger.info("Starting Bildschirm")

    try:
        logger.info("Loading Config")
        config = Config(toml.load("config.toml"))
    except FileNotFoundError:
        logger.warn("Config not found falling back to defaults")
        config = Config()
    except Exception as e:
        logger.error("While Loading Config: " + str(e))
        sys.exit(127)

    logger.info("Using {} as GUI".format(config.screen.gui))

    if config.screen.gui == "Qt":
        logger.debug("Importing required packages for Qt")
        from PyQt5.QtWidgets import QApplication
        from qtslide import Slideshow

        logger.debug("Creating QApplication")
        try:
            app = QApplication(sys.argv)
        except Exception as e:
            logger.exception(e)
            sys.exit(127)

        logger.debug("Creating QtSlideshow")
        try:
            slideshow = Slideshow(app, config)
            slideshow.start()
        except Exception as e:
            logger.exception(e)
            sys.exit(127)

        try:
            code = app.exec_()
        except Exception as e:
            logger.exception(e)
            sys.exit(127)
        logger.info("Exiting with " + str(code))
        sys.exit(code)
    elif config.screen.gui == "Tk":
        logger.debug("Importing required packages for Tk")
        from tkslide import Slideshow

        logger.debug("Creating TkSlideshow")
        try:
            slideshow = Slideshow(config)
            slideshow.start()
            logger.info("Exiting")
            sys.exit(0)
        except Exception as e:
            logger.exception(e)
            sys.exit(127)
    else:
        logger.error("Invalid GUI Type: " + config.screen.gui +
                     " screen.gui should be one of Qt, Tk")
        sys.exit(127)


if __name__ == "__main__":
    main()
