# GameRound - контейнер состояния 1 раунда игры
# описание одного игрового раунда:
# слово, количество оставшихся попыток, история введённых слов, результаты проверок
from logic.word import Word


class GameRound:
    def __init__(self, word: Word, attempts: int):
        self.word = word
        self.attempts_left = attempts
        self.guesses = []  # список введённых слов
        self.results = []  # результаты проверок

    def add_guess(self, guess: str, result: list):
        self.guesses.append(guess)
        self.results.append(result)
        self.attempts_left -= 1