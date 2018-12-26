import glob
import os.path


def get_files(path, extensions):
    result = list()
    path += "/**"
    for filename in glob.glob(path, recursive=True):
        _, ext = os.path.splitext(filename)
        if ext.lower() in extensions:
            result.append(os.path.normpath(filename))
    return result
