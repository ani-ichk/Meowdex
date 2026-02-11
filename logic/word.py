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

    def check_guess(self, guess: str):
        """
        Сравнивает guess с self.value
        Возвращает список состояний для каждой буквы: 'correct', 'present', 'absent'
        """
        guess = guess.lower()
        result = ["absent"] * self.length
        target_letters = list(self.value)

        # Сначала правильные позиции
        for i in range(self.length):
            if i < len(guess) and guess[i] == target_letters[i]:
                result[i] = "correct"
                target_letters[i] = None

        # Потом буквы в слове, но не на месте
        for i in range(self.length):
            if i >= len(guess) or result[i] == "correct":
                continue
            if guess[i] in target_letters:
                result[i] = "present"
                target_letters[target_letters.index(guess[i])] = None

        return result
