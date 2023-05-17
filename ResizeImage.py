from PIL import Image
import os
import sys

def resize_background(canvas_w, canvas_h, imageURL):
    image = Image.open(imageURL)   
    resized = image.resize((canvas_w, canvas_h),  resample=Image.NEAREST)
    return resized

def resize_sprites(factor, imageURL):
    image = Image.open(imageURL)
    w = image.width * factor
    h = image.height * factor
    resized = image.resize((w, h), resample=Image.NEAREST)
    return resized


def mirror_sprite(image):
    return image.transpose(method=Image.FLIP_LEFT_RIGHT)


def getAbsPath(filename):
    exe_dir = os.path.dirname(sys.argv[0])
    assets_dir = os.path.join(exe_dir, "assets")
    asset_path = os.path.join(assets_dir, filename)
    return asset_path
    
