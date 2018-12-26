#!/usr/bin/env python3
"""Display a slideshow from a list of filenames"""

import random
import tkinter

from PIL import Image, ImageTk

from config import Config
from util import get_files

from logger import create_logger
logger = create_logger(__name__)


class Slideshow(tkinter.Tk):
    """Display a slideshow"""

    allowed_extensions = [".png", ".jpg", ".jpeg"]
    images = list()
    history = list()
    history_pointer = 0
    config: Config

    def __init__(self, _config: Config):
        tkinter.Tk.__init__(self)
        logger.debug("Creating Window")
        self.config = _config

        logger.debug("Setting geometry to +0+0")
        self.geometry("+0+0")

        logger.info("Setting Topmost to " + self.config.slideshow.topmost)
        self.attributes("-topmost", self.config.slideshow.topmost)

        logger.info("Setting Fullscreen to " +
                    self.config.slideshow.fullscreen)
        self.attributes("-fullscreen", self.config.slideshow.fullscreen)

        logger.debug("image_path: " + self.config.screen.image_path)
        self.image_path = self.config.screen.image_path
        logger.debug("interval: " + self.config.slideshow.interval)
        self.interval = self.config.slideshow.interval
        logger.debug("max_history_length: " +
                     self.config.slideshow.history_length)
        self.max_history_length = self.config.slideshow.history_length

        logger.debug("Setting Background to black")
        self.configure(background="black", cursor="none")

        logger.debug("Creating Slide Label")
        self.slide = tkinter.Label(self)
        logger.debug("Setting Slide Background to black")
        self.slide.configure(background="black")
        self.slide.pack()

        logger.debug("Bind Left")
        self.bind("<Left>", self.on_left)
        logger.debug("Bind Right")
        self.bind("<Right>", self.on_right)
        logger.debug("Bind Escape")
        self.bind("<Escape>", self.on_esc)
        logger.debug("Bind q")
        self.bind("q", self.on_esc)

    def on_left(self, event):
        self.prev_image()

    def on_right(self, event):
        self.next_image()

    def on_esc(self, event):
        self.quit()

    def load_images(self):
        logger.info(f"Getting all files in {self.image_path} with allowed"
                    f"endings ({self.allowed_extension})")
        self.images = get_files(self.image_path, self.allowed_extensions)
        self.shuffle_images()

    def shuffle_images(self):
        logger.info("Shuffeling Images")
        random.shuffle(self.images)

    def prepare_image_list(self):
        i = 0
        while True:
            if i >= len(self.images):
                self.shuffle_images()
                i = 0
            yield self.images[i]
            i += 1

    def select_image(self):
        if not hasattr(self, "image_list"):
            self.image_list = self.prepare_image_list()
        return self.image_list.__next__()

    def next_image(self):
        logger.info("Loading next Image")

        # if the history pointer is 0 we're at the top an will load a new image
        # otherwise we increase the pointer and load the next image
        if self.history_pointer == 0:
            self.image_name = self.select_image()
        else:
            self.history_pointer -= 1
            self.image_name = self.history[-self.history_pointer]

        # add image to history
        self.history.append(self.image_name)

        # ensure history is not longer than we want
        if len(self.history) > self.max_history_length:
            self.history = self.height[len(self.history) - self.max_history_length:]

        # load the image
        self.load_image()

        self.schedule_next_image()

    """
    Load the previous image

    Get the image path from our history
    """
    def prev_image(self):
        logger.info("Loading previous Image")

        if self.history_pointer >= self.max_history_length:
            self.history_pointer = self.max_history_length

        # move deeper into the history
        self.history_pointer += 1

        # an get the image name
        self.image_name = self.history[-self.history_pointer]

        # and load it
        self.load_image()

        self.schedule_next_image()

    def load_image(self):
        logger.info(f"Loading {self.image_name}")

        # actually load the image from the given path
        self.image = Image.open(self.image_name)

        logger.debug("Loaded Image Size: "
                     f"{self.image.width}x{self.image.height}")

        if self.image.width > 1920 or self.image.height > 1080:
            wscale = 1920 / self.image.width
            hscale = 1080 / self.image.height
            if wscale > hscale:
                scale = hscale
            else:
                scale = wscale

            new_width = int(scale * self.image.width)
            new_height = int(scale * self.image.height)

            logger.info(f"Resizing image to W: {new_width} H: {new_height}.")

            self.image = self.image.resize((new_width, new_height),
                                           Image.LANCZOS)

        self.image = ImageTk.PhotoImage(self.image)

        # load the image as image of slide
        self.slide.config(image=self.image)

        # set the title (could be removed but who cares)
        self.title(self.image_name)

        # center the slide
        self.center()

    def center(self):
        """Center the image in the window"""
        logger.debug("Centering Slide")

        self.update_idletasks()
        self.slide.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

    def schedule_next_image(self):
        if hasattr(self, "next_image_alarm"):
            self.after_cancel(getattr(self, "next_image_alarm"))
        self.next_image_alarm = self.after(self.interval, self.next_image)

    def start(self):
        """Start method"""
        self.load_images()
        self.next_image()
        self.mainloop()
