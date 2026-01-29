import arcade
from ui.screens.result_screen import ResultScreen


class GameScreen(arcade.View):
    def __init__(self, word, mode, difficulty):
        super().__init__()
        self.word = word
        self.mode = mode
        self.difficulty = difficulty

        self.word_length = len(self.word.word)
        self.max_attempts = self.word_length + 1
        self.rows = 6
        self.grid = [["" for _ in range(self.word_length)] for _ in range(self.rows)]

        self.current_row = 0
        self.current_col = 0

    def check_word(self):
        guess = "".join(self.grid[self.current_row]).lower()
        result = self.word.check_guess(guess)

        for i, status in enumerate(result):
            letter = guess[i].upper()

            if status == "correct":
                texture_name = f"З_{letter}"
            elif status == "present":
                texture_name = f"О_{letter}"
            else:
                texture_name = f"Ч_{letter}"

        self.current_row += 1
        self.current_col = 0

    def on_key_press(self, key, modifiers):
        if arcade.key.A <= key <= arcade.key.Z:
            if self.current_col < self.word_length:
                self.grid[self.current_row][self.current_col] = chr(key)
                self.current_col += 1

        elif key == arcade.key.BACKSPACE and self.current_col > 0:
            self.current_col -= 1
            self.grid[self.current_row][self.current_col] = ""

        elif key == arcade.key.ENTER:
            self.check_word()

    def end_game(self, result):
        fish = 0
        if result == "win":
            fish = 3
        elif result == "draw":
            fish = 1

        self.window.show_view(
            ResultScreen(result, fish)
        )

