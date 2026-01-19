# модель загаданного слова и состояние его угадывания:
# само слово, сравнение попыток с загаданным, результат проверки букв (зелёный/ж/к)
class Word:
    def __init__(self, word):
        self.word = word

    def check_guess(self, guess: str):
        result = []
        guess = guess

        for i, letter in enumerate(guess):
            if letter == self.word[i]:
                result.append("correct")
            elif letter in self.word:
                result.append("present")
            else:
                result.append("absent")

        return result