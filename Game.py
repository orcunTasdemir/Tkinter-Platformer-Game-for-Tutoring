from tkinter import *
from PIL import Image, ImageTk
import random
import time
from ResizeImage import *
import Coords
from Sprite import *


class Game:
    def __init__(self):
        self.tk = Tk()
        self.scale = 5
        self.gravity = 1.6
        self.tk.title("Platformer Game")
        # so the screen is not resizable 0 means "False"
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas_height = 800
        self.canvas_width = 1000
        self.canvas = Canvas(
            self.tk,
            width=self.canvas_width,
            height=self.canvas_height,
            highlightthickness=0,
        )
        self.canvas.pack()
        self.tk.update()
        self.bg = ImageTk.PhotoImage(
            resize_background(
                self.canvas_width,
                self.canvas_height,
                "assets/gameElements/backgrounds/background.png",
            )
        )
        bg_w = self.bg.width()
        bg_h = self.bg.height()

        self.canvas.create_image(0, 0, image=self.bg, anchor="nw")
        self.sprites = []
        self.running = True

    def mainloop(self):
        while True:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            if self.running == False:
                self.canvas.create_text(
                    self.canvas_width / 2,
                    self.canvas_height / 2 - 200,
                    text="You win",
                    fill="orange",
                    font=("Helvetica 85 bold"),
                )
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


# initiate the game here
g = Game()
# add some platforms to the game
platforms = [
    PlatformSprite(g, "long", 700, 150),  # finish platform
    PlatformSprite(g, "medium", 680, 645), #first
    PlatformSprite(g, "medium", 410, 500), #second
    PlatformSprite(g, "short", 120, 350), #third
    PlatformSprite(g, "medium", 340, 210),
]

# add a door at the top as the objective of the game (exact math to put door on the right edge of a long platform)
door = DoorSprite(
    g, "door_closed", 700 + (52 * g.scale) - (13 * g.scale), 150 - (23 * g.scale), True
)


character = CharacterSprite(g, 800, 800 - (16 * g.scale), True)

# add all to the sprites array of the game
g.sprites.extend(platforms)
g.sprites.append(door)
g.sprites.append(character)

g.mainloop()
