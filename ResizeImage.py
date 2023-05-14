from PIL import Image


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
    
