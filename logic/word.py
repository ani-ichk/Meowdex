# модель загаданного слова и состояние его угадывания:
# само слово, сравнение попыток с загаданным, результат проверки букв (зелёный/ж/к)
import json
import random
from pathlib import Path

class Word:
    def __init__(self, value: str):
        self.value = value.lower()
        self.length = len(self.value)

    @staticmethod
    def random_by_difficulty(difficulty: str):
        path = Path("data/words/words.json")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        word = random.choice(data[difficulty])
        return word

