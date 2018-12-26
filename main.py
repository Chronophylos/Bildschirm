from config import Config
import toml
import sys


def main():
    try:
        config = Config(toml.load("config.toml"))
    except toml.TomlDecodeError as e:
        print(e)
        return

    if config.screen.slide == "Qt":
        from PyQt5.QtWidgets import QApplication
        from qtslide import Slideshow

        app = QApplication([])
        slideshow = Slideshow(config)
        slideshow.start()
        sys.exit(app.exec_())
    elif config.screen.slide == "Tk":
        from tkslide import Slideshow
        slideshow = Slideshow(config)
        slideshow.start()


if __name__ == "__main__":
    main()
