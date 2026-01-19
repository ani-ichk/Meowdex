# координатор, какой контроллер активен, какой экран показывать
from game_state import GameState
from menu_controller import MenuController
from ui.screens.menu_screen import MenuScreen


class AppController:
    def __init__(self):
        self.state = GameState()
        self.current_controller = None
        self.current_screen = None

    def set_menu(self):
        self.current_controller = MenuController()
        self.current_screen = MenuScreen()

    def get_event(self, event):
        pass