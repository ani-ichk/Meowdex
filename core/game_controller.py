# запуск раундов, обработка ходов, победа/поражение, награды
class GameController:
    def __init__(self, app):
        self.app = app

    def start_round(self):
        word = load_word(self.app.state.difficulty)
        self.round = Round(word)