from MainGame.screens.screen import Screen
import pyglet
from pyglet.text import Label as pyglLabel

"""
Main game container
"""
class Game:
    CLICKREVEAL=1
    CLICKFLAG=2
    def __init__(self, mine_locs, board_type, graphics_container_type):
        self.display_batch = pyglet.graphics.Batch()
        self.text_batch = pyglet.graphics.Batch()
        self.board = board_type(mine_locs)
        self.graphics = [graphics_container_type(tile, self.display_batch, self.text_batch) for tile in self.board.tiles]
    
    def display(self):
        for tile_graphics in self.graphics:
            tile_graphics.update_graphics()
        self.display_batch.draw()
        self.text_batch.draw()

    def on_click(self, x, y, type_):
        real_x=(x-self.graphics[0].OFFSET[0])/self.graphics[0].SCALE
        real_y=(y-self.graphics[0].OFFSET[1])/self.graphics[0].SCALE
        if type_==Game.CLICKREVEAL: return (self.board.on_click(real_x, real_y, self.board.CLICKREVEAL))
        return self.board.on_click(real_x, real_y, self.board.CLICKFLAG)

"""
Screen class for the main game.
Requires board type, graphics definition, and mine locations
"""
class GameScreen(Screen):
    def __init__(self, mine_locs, board_type, graphics_container_type, **kwargs):
        super().__init__(self)
        self.game = Game(mine_locs, board_type, graphics_container_type)
        self.complete = False

    def on_click(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            if not self.complete and not self.game.on_click(x, y, Game.CLICKREVEAL): # Clicked a mine
                self.on_loss()

            if self.complete:
                if x >= 487 and x <= 537 and y >= 205 and y <= 235: self.on_exit()

        if button == pyglet.window.mouse.RIGHT:
            if not self.complete: self.game.on_click(x, y, Game.CLICKFLAG)

    def on_exit(self):
        pyglet.app.exit()

    def on_loss(self):
        self.complete = True
        self.complete_label = pyglLabel(text="You Lose!", font_size=32, anchor_x="center", anchor_y="center", x=512, y=256)
        self.exit_label = pyglLabel(text="Exit", font_size=20, anchor_x="center", anchor_y="center", x=512, y=220)
        self.exit_button = pyglet.shapes.Rectangle(487, 205, 50, 30, color=(0,0,0))

    def display(self, window):
        window.clear()
        self.game.display()
        if self.complete: 
            self.complete_label.draw()
            self.exit_button.draw()
            self.exit_label.draw()

    def switch_screen(self, other_screen):
        super().switch_screen(other_screen)