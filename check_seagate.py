
import sys
from util import get_files
from pprint import pprint
import time
import humanize


start = time.time()
files = get_files("//SEAGATE-DP4/Bilder/Fotos", [".png", ".jpg", ".jpeg"])
#files = get_files("D:/Work/Wallpaper", [".png", ".jpg", ".jpeg"])
diff = time.time() - start
size = sys.getsizeof(files)
perc = 20000 / len(files)
#pprint(files)
print(f"time to get all files: {diff} s time per file: {diff / len(files)}")
print(f"files: {len(files)} total size: {humanize.naturalsize(size)} per image: {humanize.naturalsize(size / len(files))}")
print(f"predictions for 20000 files: time: {diff * perc} s size: {humanize.naturalsize(size * perc)}")