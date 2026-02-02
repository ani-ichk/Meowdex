import arcade
from logic.progress import Progress
from ui.screens.result_screen import ResultScreen

WIDTH = 800
HEIGHT = 600


class GameScreen(arcade.View):
    def __init__(self, target_word: str, difficulty, mode="single"):
        super().__init__()
        self.target_word = target_word.upper()
        self.difficulty = difficulty
        self.mode = mode

        self.attempts_left = difficulty.attempts
        self.current_input = ""
        self.guesses = []

        self.game_over = False
        self.result_text = ""

    # ---------- INPUT ----------
    def on_key_press(self, symbol, modifiers):
        if self.game_over:
            return

        if symbol == arcade.key.ENTER:
            self.submit_word()
            return

        if symbol == arcade.key.BACKSPACE:
            self.current_input = self.current_input[:-1]
            return

        char = chr(symbol).upper()
        if "А" <= char <= "Я":
            if len(self.current_input) < len(self.target_word):
                self.current_input += char

    # ---------- GAME LOGIC ----------
    def submit_word(self):
        if len(self.current_input) != len(self.target_word):
            return

        guess = self.current_input
        self.guesses.append(guess)
        self.current_input = ""
        self.attempts_left -= 1

        if guess == self.target_word:
            self.finish_game(win=True)
        elif self.attempts_left == 0:
            self.finish_game(win=False)

    def on_win(self):
        progress = Progress.load()
        progress.add_fish(self.difficulty.reward)
        progress.save()

        self.window.show_view(ResultScreen(
            status="win",
            reward=self.difficulty.reward
        ))

    def finish_game(self, win: bool):
        self.game_over = True

        if win:
            self.result_text = "ПОБЕДА 🎉"

            if self.mode == "single":
                progress = Progress.load()
                progress.fish += self.difficulty.reward
                progress.save()
        else:
            self.result_text = f"ПОРАЖЕНИЕ 😿\nСлово: {self.target_word}"

    # ---------- LETTER CHECK ----------
    def check_letter(self, letter, index):
        if self.target_word[index] == letter:
            return "correct"
        elif letter in self.target_word:
            return "present"
        return "absent"

    # ---------- DRAW ----------
    def on_draw(self):
        self.clear()

        arcade.draw_text(
            f"Попытки: {self.attempts_left}",
            20, HEIGHT - 40,
            arcade.color.WHITE, 18
        )

        y = HEIGHT - 100
        for guess in self.guesses:
            x = 200
            for i, letter in enumerate(guess):
                status = self.check_letter(letter, i)
                color = {
                    "correct": arcade.color.GREEN,
                    "present": arcade.color.YELLOW,
                    "absent": arcade.color.GRAY
                }[status]

                arcade.draw_text(letter, x, y, color, 24)
                x += 40
            y -= 40

        arcade.draw_text(
            self.current_input,
            200, y,
            arcade.color.WHITE, 24
        )

        if self.game_over:
            arcade.draw_text(
                self.result_text,
                WIDTH // 2 - 150,
                HEIGHT // 2,
                arcade.color.ORANGE,
                28
            )
