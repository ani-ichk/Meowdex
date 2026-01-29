# модель загаданного слова и состояние его угадывания:
# само слово, сравнение попыток с загаданным, результат проверки букв (зелёный/ж/к)
import json
import random
from pathlib import Path

class Word:
    def __init__(self, word):
        self.word = word

    def check_guess(self, guess: str):
        result = []
        for i, letter in enumerate(guess):
            if letter == self.word[i]:
                result.append("correct")
            elif letter in self.word:
                result.append("present")
            else:
                result.append("absent")
        return result

    @classmethod
    def random_by_difficulty(cls, difficulty: str):
        path = f"data/words/{difficulty}.json"
        with open(path, "r", encoding="utf-8") as f:
            words = json.load(f)

        return cls(random.choice(words))

    def get_random_word(difficulty: str) -> str:
        """
        Возвращает случайное слово из json-файла по сложности
        """
        path = Path("data/words") / f"{difficulty}.json"

        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        words = data["words"]
        return random.choice(words)

