from PIL import Image
from ResizeImage import *

imageURL = getAbsPath("gameElements/doors/doors.png")
im = Image.open(imageURL)
closedDoor = im.crop((0, 0, 13, 23))
idx = imageURL.index(".png")
newURL = imageURL[:idx] + "_closed" + imageURL[idx:]
closedDoor.save(newURL)

im = Image.open(imageURL)
openDoor = im.crop((0, 23, 13, 47))
idx = imageURL.index(".png")
newURL = imageURL[:idx] + "_open" + imageURL[idx:]
openDoor.save(newURL)