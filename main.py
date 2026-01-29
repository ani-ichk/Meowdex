# ================= DPI FIX =================
# Чинит проблему масштабирования Windows
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)


import arcade
from ui.screens.menu_screen import MenuScreen


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Meowdex"


class MainWindow(arcade.Window):
    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)

    def setup(self):
        self.show_view(MenuScreen())


def main():
    window = MainWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()