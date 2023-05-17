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
            "short": ImageTk.PhotoImage(
                resize_sprites(
                    game.scale, getAbsPath("gameElements/platforms/platforms_short.png")
                )
            ),
            "medium": ImageTk.PhotoImage(
                resize_sprites(
                    game.scale, getAbsPath("gameElements/platforms/platforms_medium.png")
                )
            ),
            "long": ImageTk.PhotoImage(
                resize_sprites(
                    game.scale, getAbsPath("gameElements/platforms/platforms_long.png")
                )
            ),
        }
        self.imageSelect = self.images[imageName]
        self.imageCoords = self.game.canvas.create_image(
            x, y, image=self.imageSelect, anchor="nw"
        )
        self.coordinates = Coords(
            x, y, x + self.imageSelect.width(), y + self.imageSelect.height()
        )


class DoorSprite(Sprite):
    def __init__(self, game, imageName, x, y, isClosed):
        Sprite.__init__(self, game)
        self.endgame = True
        self.isClosed = isClosed
        self.images = {
            "door_open": ImageTk.PhotoImage(
                resize_sprites(game.scale, getAbsPath("gameElements/doors/doors_open.png"))
            ),
            "door_closed": ImageTk.PhotoImage(
                resize_sprites(game.scale,getAbsPath( "gameElements/doors/doors_closed.png"))
            ),
        }

        self.imageSelect = self.images[imageName]
        self.imageCoords = self.game.canvas.create_image(
            x, y, image=self.imageSelect, anchor="nw"
        )
        self.coordinates = Coords(
            x, y, x + self.imageSelect.width(), y + self.imageSelect.height()
        )

    def animate(self):
        self.game.canvas.itemconfig(self.imageCoords, image=self.images["door_open"])


class CharacterSprite(Sprite):
    def __init__(self, game, x, y, facingLeft):
        Sprite.__init__(self, game)
        self.facingLeft = facingLeft
        self.images_right = [
            ImageTk.PhotoImage(
                resize_sprites(
                    game.scale, getAbsPath("character/characterSprites_first_stance.png")
                )
            ),
            ImageTk.PhotoImage(
                resize_sprites(
                    game.scale, getAbsPath("character/characterSprites_second_stance.png")
                )
            ),
            ImageTk.PhotoImage(
                resize_sprites(
                    game.scale, getAbsPath("character/characterSprites_third_stance.png")
                )
            ),
        ]
        self.images_left = [
            ImageTk.PhotoImage(
                mirror_sprite(
                    resize_sprites(
                        game.scale, getAbsPath("character/characterSprites_first_stance.png")
                    )
                )
            ),
            ImageTk.PhotoImage(
                mirror_sprite(
                    resize_sprites(
                        game.scale,
                        getAbsPath("character/characterSprites_second_stance.png"),
                    )
                )
            ),
            ImageTk.PhotoImage(
                mirror_sprite(
                    resize_sprites(
                        game.scale, getAbsPath("character/characterSprites_third_stance.png")
                    )
                )
            ),
        ]
        self.imageSelect = self.images_left[1] if facingLeft else self.images_right[1]
        self.imageCoords = self.game.canvas.create_image(
            x, y, image=self.imageSelect, anchor="nw"
        )
        self.imageIdx = 1

        self.coordinates = Coords(
            x, y, x + self.imageSelect.width(), y + self.imageSelect.height()
        )
        self.x = 0
        self.y = 0
        self.terminal = 30
        self.speed = 20
        self.jump_v = -30
        self.direction = "stop"
        self.jump_count = 0
        self.jump_duration = 12
        self.last_time = time.time()
        game.canvas.bind_all("<KeyPress-Left>", self.setDirection)
        game.canvas.bind_all("<KeyPress-Right>", self.setDirection)
        game.canvas.bind_all("<KeyRelease-Left>", self.setStop)
        game.canvas.bind_all("<KeyRelease-Right>", self.setStop)
        game.canvas.bind_all("<space>", self.jump)

    def setDirection(self, evt):
        self.direction = evt.keysym

    def setStop(self, evt):
        self.direction = "stop"

    def getDirection(self):
        if self.direction == "Left":
            self.x = -self.speed
        if self.direction == "Right":
            self.x = self.speed
        if self.direction == "stop":
            self.x = 0

    def jump(self, evt):
        # can jump only when you are not jumping already or falling
        if self.y == 0:
            self.y = self.jump_v

    def animate(self):
        if self.x < 0:
            self.facingLeft = True
        elif self.x > 0:
            self.facingLeft = False
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.05:
                self.last_time = time.time()
                self.imageIdx = (self.imageIdx + 1) % 2
        if self.facingLeft:
            if self.y != 0:
                self.game.canvas.itemconfig(self.imageCoords, image=self.images_left[0])
            else:
                if self.x < 0:
                    self.game.canvas.itemconfig(
                        self.imageCoords, image=self.images_left[self.imageIdx]
                    )
                else:
                    self.game.canvas.itemconfig(self.imageCoords, image=self.images_left[1])

        elif not self.facingLeft:
            if self.y != 0:
                self.game.canvas.itemconfig(self.imageCoords, image=self.images_right[0])
            else:
                if self.x > 0:
                    self.game.canvas.itemconfig(
                        self.imageCoords, image=self.images_right[self.imageIdx]
                    )
                else:
                    self.game.canvas.itemconfig(
                        self.imageCoords, image=self.images_right[1]
                    )

    def move(self):
        self.getDirection()
        self.animate()
        self.y += self.game.gravity * self.game.gravity
        co = self.coords()
        top = True
        bottom = True
        left = True
        right = True
        falling = True

        if self.y > 0 and collided_bottom_canvas(
            self.y, co.y2, self.game.canvas_height
        ):
            self.y = self.game.canvas_height - co.y2
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False
        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False

        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = self.game.gravity * self.game.gravity
                top = False
            # for when there is a platform right beneath us
            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0
                bottom = False
                top = False
            if (
                bottom
                and falling
                and self.y == 0
                and co.y2 < self.game.canvas_height
                and collided_bottom(1, co, sprite_co)
            ):
                falling = False
            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0
                left = False
                if sprite.endgame:
                    sprite.animate()
                    self.game.running = False
            if right and self.x > 0 and collided_right(co, sprite_co):
                self.x = 0
                right = False
                if sprite.endgame:
                    sprite.animate()
                    self.game.running = False
        # for when we are not on the bottom not already falling but there are no collisions
        if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
            self.y = self.game.gravity * self.game.gravity

        # there is a terminal fall velocity to not be ridiculous
        self.game.canvas.move(self.imageCoords, self.x, min(self.terminal, self.y))

    def coords(self):
        xy = self.game.canvas.coords(self.imageCoords)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + self.imageSelect.width()
        self.coordinates.y2 = xy[1] + self.imageSelect.height()
        return self.coordinates
