
from Coords import *
from PIL import ImageTk
from ResizeImage import *
import time

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
        self.imageSelect = self.images[imageName]
        self.imageCoords = self.game.canvas.create_image(x, y, image=self.imageSelect, anchor='nw')
        self.coordinates = Coords(x, y, x + self.imageSelect.width(), y + self.imageSelect.height())      
class DoorSprite(Sprite):
    def __init__(self, game, imageName, x, y, isClosed):
        Sprite.__init__(self, game)
        self.isClosed = isClosed
        self.images = {
            "door_open": ImageTk.PhotoImage(resize_sprites(game.scale, "assets/gameElements/doors/doors_open.png")),
            "door_closed": ImageTk.PhotoImage(resize_sprites(game.scale, "assets/gameElements/doors/doors_closed.png"))
        }
        
        self.imageSelect = self.images[imageName]
        self.imageCoords = self.game.canvas.create_image(x, y, image=self.imageSelect, anchor='nw')
        self.coordinates = Coords(x, y, x + self.imageSelect.width(), y + self.imageSelect.height())
        
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
        self.imageSelect = self.images_left[imageName] if facingLeft else self.images_right[imageName]
        self.imageCoords = self.game.canvas.create_image(x, y, image=self.imageSelect, anchor='nw')
        self.coordinates = Coords(x, y, x + self.imageSelect.width(), y + self.imageSelect.height())
        self.speed = 0 #the walking speed
        self.y_speed = 0 #the jumping height
        self.direction = "stop"
        self.jump_count = 0
        self.last_time = time.time()
        self.game.canvas.bind_all("<Key>", self.directionChanger)
        
    def move(self):
        print("speedx: ", self.speed, "speedy: ", self.y_speed)
        
        if self.direction != "stop":
            if self.direction == "left":
                self.speed = - 10
            elif self.direction == "right":
                self.speed = 10
            elif self.direction == "jump":
                self.y_speed = -4
                
            #self.animate()
            if self.y_speed < 0:
                self.jump_count += 1
                if self.jump_count > 20:
                    self.y_speed = 3
            if self.y_speed > 0:
                self.jump_count -= 1
            co = self.coords()
            #all start from true and get set to false when there is a collision, so do not check again
            top = True
            bottom = True
            left = True
            right = True
            falling = True
            
            if self.y_speed > 0 and co.y2 >= self.game.canvas_height:
                self.y_speed = 0
                bottom = False
            elif self.y_speed < 0 and co.y1 <= 0:
                self.y_speed = 0
                top = False
            if self.speed > 0 and co.x2 >= self.game.canvas_width:
                self.speed = 0
                right = False
            elif self.speed < 0 and co.x1 <= 0:
                self.speed = 0
                left = False
        
            for sprite in self.game.sprites:
                if sprite == self:
                    continue
                sprite_co = sprite.coords()
                #checking the top collision if there is collision, set y speed to invert and set top to false
                if top and self.y_speed < 0 and collided_top(co, sprite_co):
                    self.y_speed = - self.y_speed
                    top = False
                #check bottom collision and if there is collision set y_speed such that we land on the sprite
                #we were about to collide with and if for some reason y speed gets below 0 set it to 0
                #set top and bottom to false
                if bottom and self.y_speed > 0 and collided_bottom(self.y_speed, co, sprite_co):
                    self.y_speed = sprite_co.y1 - co.y2
                    # if self.y_speed < 0:
                    #     self.y_speed = 0
                    # bottom = False
                    # top = False
                    self.direction = "stop"
                #check to see if we are falling, set falling to false if we are not falling 
                if bottom and falling and self.y_speed == 0 and co.y2 < self.game.canvas_height and collided_bottom(1, co, sprite_co):
                    falling = False
                #check if left collision
                if left and self.speed < 0 and collided_left(co, sprite_co):
                    self.speed = 0
                    left = False
                    if sprite.endgame:
                        self.game.running = False
                if right and self.speed > 0 and collided_right(co, sprite_co):
                    self.speed = 0
                    right = False
                    if sprite.endgame:
                        self.game.running = False
            if falling and bottom and self.y_speed == 0 and co.y2 < self.game.canvas_height:
                self.y_speed = 3
            self.game.canvas.move(self.imageCoords, self.speed, self.y_speed)
        
    def directionChanger(self, event):
        print("here")
        if event.char == "a":
            self.direction = "left"
        elif event.char == "d":
            self.direction = "right"
        elif event.char == "w":
            self.direction = "jump"
            
    def jump(self, evt):
        pass
        
    def coords(self):
        xy = self.game.canvas.coords(self.imageCoords)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + self.imageSelect.width() +5
        self.coordinates.y2 = xy[1] + self.imageSelect.height() +5
        return self.coordinates        