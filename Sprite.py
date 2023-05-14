
from Coords import *
from PIL import ImageTk
from ResizeImage import *

class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None
    def move(self):
        pass
    def coords(self):
        return self.coordinates
    
    
    
class PlatformSprite(Sprite):
    def __init__(self, game, imageName, x, y):
        Sprite.__init__(self, game)
        self.images = {
            "short" : ImageTk.PhotoImage(resize_sprites(game.scale, "assets/gameElements/platforms/platforms_short.png")),
            "medium" : ImageTk.PhotoImage(resize_sprites(game.scale, "assets/gameElements/platforms/platforms_medium.png")),
            "long" : ImageTk.PhotoImage(resize_sprites(game.scale, "assets/gameElements/platforms/platforms_long.png"))
                }
        self.image = self.images[imageName]
        self.game.canvas.create_image(x, y, image=self.image, anchor='nw')
        self.coordinates = Coords(x, y, x + self.image.width(), y + self.image.height())
        
class DoorSprite(Sprite):
    def __init__(self, game, imageName, x, y, isClosed):
        Sprite.__init__(self, game)
        self.isClosed = isClosed
        self.images = {
            "door_open": ImageTk.PhotoImage(resize_sprites(game.scale, "assets/gameElements/doors/doors_open.png")),
            "door_closed": ImageTk.PhotoImage(resize_sprites(game.scale, "assets/gameElements/doors/doors_closed.png"))
        }
        
        self.image = self.images[imageName]
        self.game.canvas.create_image(x, y, image=self.image, anchor='nw')
        self.coordinates = Coords(x, y, x + self.image.width(), y + self.image.height())
        
class CharacterSprite(Sprite):
    def __init__(self, game, imageName, x, y, facingLeft):
        Sprite.__init__(self, game)
        self.facingLeft = facingLeft
        self.images_right = {
            "first" : ImageTk.PhotoImage(resize_sprites(game.scale, "assets/character/characterSprites_first_stance.png")),
            "second" : ImageTk.PhotoImage(resize_sprites(game.scale, "assets/character/characterSprites_second_stance.png")),
            "third" : ImageTk.PhotoImage(resize_sprites(game.scale, "assets/character/characterSprites_third_stance.png"))
        }
        self.images_left = {
            "first" : ImageTk.PhotoImage(mirror_sprite(resize_sprites(game.scale, "assets/character/characterSprites_first_stance.png"))),
            "second" : ImageTk.PhotoImage(mirror_sprite(resize_sprites(game.scale, "assets/character/characterSprites_second_stance.png"))),
            "third" : ImageTk.PhotoImage(mirror_sprite(resize_sprites(game.scale, "assets/character/characterSprites_third_stance.png")))
        }
        self.image = self.images_left[imageName] if facingLeft else self.images_right[imageName]
        self.game.canvas.create_image(x, y, image=self.image, anchor='nw')
        self.coordinates = Coords(x, y, x + self.image.width(), y + self.image.height())