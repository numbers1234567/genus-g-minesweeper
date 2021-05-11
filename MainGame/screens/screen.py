
"""
Generic class for screen for use by the main window function
"""
class Screen:
    def __init__(self, window, **kwargs):
        self.window = window

    def on_click(self, x, y, button, modifiers):
        pass

    def display(self):
        pass

    def switch_screen(self, other_screen):
        self.window.set_screen(other_screen)

    def on_key_press(self, symbol, modifiers):
        pass