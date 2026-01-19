# модель уровня сложности: параметры слов, попыток и наград
class Difficulty:
    def __init__(self, name, min_len, max_len, attempts, reward):
        self.name = name
        self.min_len = min_len
        self.max_len = max_len
        self.attempts = attempts
        self.reward = reward