import glob
import os.path
import random


def get_files(path, extensions):
    result = list()
    path += "/**"
    for filename in glob.glob(path, recursive=True):
        _, ext = os.path.splitext(filename)
        if ext.lower() in extensions:
            result.append(os.path.normpath(filename))
    return result

def getExif(image):
     exif = {}
     info = image._getexif()
     for tag, value in info.items():
         decoded = TAGS.get(tag, tag)
         exif[decoded] = value
     return exif

class History:
    """
    Simple History List
    """

    cursor = 0
    _list = list()

    def __init__(self, maxlen):
        self.maxlen = maxlen

    def current(self):
        return self._list[self.cursor]

    def next(self):
        if self.hasNext():
            self.cursor += 1
            return self.current()

    def prev(self):
        if self.hasPrev():
            self.cursor -= 1
            return self.current()

    def hasNext(self):
        return self.cursor < len(self._list) - 1

    def hasPrev(self):
        return self.cursor > 0

    def push(self, x):
        """
        Add a new element to the History

        Removes last element if max lenght is reached.
        Set the pointer to the first element.
        """
        # if the list is at max lenght
        if len(self._list) >= self.maxlen:
            # remove the last element
            self._list.pop(0)

        # add the new element
        self._list.append(x)

        # set the pointer to the first element
        self.cursor = len(self._list) - 1

    def size(self):
        return len(self._list)


class RandomImageList:
    cursor = 0

    def __init__(self, _list):
        self._list = _list
        self.shuffle()

    def next(self):
        if self.cursor >= len(self._list):
            self.shuffle()
        x = self._list[self.cursor]
        self.cursor += 1
        return x

    def shuffle(self):
        self.cursor = 0
        random.shuffle(self._list)
