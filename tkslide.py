#!/usr/bin/env python3
"""Display a slideshow from a list of filenames"""

import glob
import os
import os.path
import random
import tkinter
from collections import deque
from itertools import cycle

from PIL import Image, ImageTk

from config import Config
from util import get_files


class Slideshow(tkinter.Tk):
    """Display a slideshow"""

    allowed_extensions = [".png", ".jpg", ".jpeg"]
    images = list()
    history = list()
    history_pointer = 0
    config: Config

    def __init__(self, _config: Config):
        tkinter.Tk.__init__(self)
        self.config = _config

        self.geometry("+0+0")
        self.attributes("-topmost", self.config.slideshow.topmost)
        self.attributes("-fullscreen", self.config.slideshow.fullscreen)

        self.image_path = self.config.screen.image_path
        self.interval = self.config.slideshow.interval
        self.max_history_length = self.config.slideshow.history_length

        self.configure(background="black", cursor="none")

        self.slide = tkinter.Label(self)
        self.slide.configure(background="black")
        self.slide.pack()

        self.bind("<Left>", self.on_left)
        self.bind("<Right>", self.on_right)
        self.bind("<Escape>", self.on_esc)
        self.bind("q", self.on_esc)

    def on_left(self, event):
        self.prev_image()
    
    def on_right(self, event):
        self.next_image()
    
    def on_esc(self, event):
        self.quit()
    
    def load_images(self):
        print("Populating image list")
        self.images = get_files(self.image_path, self.allowed_extensions)
        self.shuffle_images()

    def shuffle_images(self):
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
        # actually load the image from the given path
        self.image = Image.open(self.image_name)

        print(f"Loading {self.image_name} W: {self.image.width} H: {self.image.width}.")

        if self.image.width > 1920 or self.image.height > 1080:
            wscale = 1920 / self.image.width 
            hscale = 1080 / self.image.height
            if wscale > hscale:
                scale = hscale
            else:
                scale = wscale

            new_width = int(scale * self.image.width)
            new_height = int(scale * self.image.height)

            print(f"Resizing image to W: {new_width} H: {new_height}.")
            
            self.image = self.image.resize((new_width, new_height), Image.LANCZOS)

        self.image = ImageTk.PhotoImage(self.image)

        # load the image as image of slide
        self.slide.config(image=self.image)

        # set the title (could be removed but who cares)
        self.title(self.image_name)

        # center the slide
        self.center()
    
    def center(self):
        """Center the image in the window"""
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
