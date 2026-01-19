# логика главного меню
class MenuController:
    def __init__(self, app):
        self.app = app

    def get_event(self, event):
        if event == "start_game":
            self.app.set_game()