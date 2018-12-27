import sys
from util import get_files

files = get_files("D:/Work/Wallpaper", [".png", ".jpg", ".jpeg"])
size = sys.getsizeof(files)
avg = size / len(files)
prediction = int(20000 * avg) / 1024
print(f"total: {size} B per image: {avg} B")
print(f"predicting size of: {prediction} kiB")