# модель уровня сложности: параметры слов, попыток и наград

class Difficulty:
    def __init__(self, name, attempts, reward):
        self.name = name
        self.attempts = attempts
        self.reward = reward


EASY = Difficulty("easy", 10, 1)
MEDIUM = Difficulty("medium", 8, 2)
NORMAL = Difficulty("normal", 7, 3)
HARD = Difficulty("hard", 6, 4)
EXPERT = Difficulty("expert", 5, 6)
