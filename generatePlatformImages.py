from PIL import Image
from ResizeImage import *

imageURL = getAbsPath("gameElements/platforms/platforms.png")
im = Image.open(imageURL)
longPlatform = im.crop((0, 0, 52, 6))
idx = imageURL.index(".png")
newURL = imageURL[:idx] + "_long" + imageURL[idx:]
longPlatform.save(newURL)

im = Image.open(imageURL)
shortPlatform = im.crop((0, 6, 27, 12))
idx = imageURL.index(".png")
newURL = imageURL[:idx] + "_short" + imageURL[idx:]
shortPlatform.save(newURL)

im = Image.open(imageURL)
medimuPlatform = im.crop((0, 12, 39, 18))
idx = imageURL.index(".png")
newURL = imageURL[:idx] + "_medium" + imageURL[idx:]
medimuPlatform.save(newURL)
    
    
