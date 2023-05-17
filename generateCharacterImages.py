from PIL import Image
from ResizeImage import *

imageURL = (getAbsPath("character/characterSprites.png"))
im = Image.open(imageURL)
firstStance = im.crop((0, 0, 10, 16))
idx = imageURL.index(".png")
newURL = imageURL[:idx] + "_first_stance" + imageURL[idx:]
firstStance.save(newURL)

im = Image.open(imageURL)
secondStance = im.crop((10, 0, 20, 16))
idx = imageURL.index(".png")
newURL = imageURL[:idx] + "_second_stance" + imageURL[idx:]
secondStance.save(newURL)

im = Image.open(imageURL)
thirdStance = im.crop((20, 0, 30, 16))
idx = imageURL.index(".png")
newURL = imageURL[:idx] + "_third_stance" + imageURL[idx:]
thirdStance.save(newURL)