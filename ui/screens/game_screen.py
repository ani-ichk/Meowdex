import arcade

STATUS_COLOR = {
    "З": arcade.color.GREEN,
    "О": arcade.color.ORANGE,
    "Ч": arcade.color.GRAY,
}

MAX_ATTEMPTS = 6
LETTER_SIZE = 36
LETTER_GAP = 50


class GameScreen(arcade.View):
    def __init__(self, target_word: str):
        super().__init__()

        # Слово
        self.target_word = target_word.upper()
        self.word_length = len(self.target_word)

        # Игра
        self.current_guess = ""
        self.guesses = []
        self.game_over = False
        self.game_result = None

        # UI
        self.ui_sprites = arcade.SpriteList()
        self.home_button = arcade.Sprite("data/images/button/home_btn.png", scale=0.5)
        self.ui_sprites.append(self.home_button)

    def on_show_view(self):
        # позиция кнопки домой (ТОЛЬКО ТУТ!)
        self.home_button.left = 10
        self.home_button.top = self.window.height - 10

    # ---------------- ПРОВЕРКА СЛОВА ----------------

    def check_word(self, guess: str):
        result = ["Ч"] * self.word_length
        used = [False] * self.word_length

        for i in range(self.word_length):
            if guess[i] == self.target_word[i]:
                result[i] = "З"
                used[i] = True

        for i in range(self.word_length):
            if result[i] == "З":
                continue
            for j in range(self.word_length):
                if not used[j] and guess[i] == self.target_word[j]:
                    result[i] = "О"
                    used[j] = True
                    break

        return result

    # ---------------- ОТПРАВКА ----------------

    def submit_word(self):
        if len(self.current_guess) != self.word_length:
            return

        result = self.check_word(self.current_guess)
        self.guesses.append((self.current_guess, result))

        if self.current_guess == self.target_word:
            self.game_result = "win"
            self.game_over = True
        elif len(self.guesses) >= MAX_ATTEMPTS:
            self.game_result = "lose"
            self.game_over = True

        self.current_guess = ""

    # ---------------- ВВОД ----------------

    def on_text(self, text):
        if self.game_over:
            return

        char = text.upper()
        if ("А" <= char <= "Я") or char == "Ё":
            if len(self.current_guess) < self.word_length:
                self.current_guess += char

    def on_key_press(self, key, modifiers):
        if key in (arcade.key.ENTER, arcade.key.NUM_ENTER):
            self.submit_word()
        elif key == arcade.key.BACKSPACE:
            self.current_guess = self.current_guess[:-1]

    def on_mouse_press(self, x, y, button, modifiers):
        if self.home_button.collides_with_point((x, y)):
            from ui.screens.play_screen import PlayScreen
            self.window.show_view(PlayScreen())

    # ---------------- ОТРИСОВКА ----------------

    def on_draw(self):
        self.clear()
        self.ui_sprites.draw()

        start_y = self.window.height - 140
        start_x = self.window.width // 2 - (self.word_length - 1) * LETTER_GAP // 2

        for row, (word, statuses) in enumerate(self.guesses):
            for i, letter in enumerate(word):
                arcade.draw_text(
                    letter,
                    start_x + i * LETTER_GAP,
                    start_y - row * 60,
                    STATUS_COLOR[statuses[i]],
                    LETTER_SIZE,
                    anchor_x="center",
                    anchor_y="center",
                )

        if not self.game_over:
            row = len(self.guesses)
            for i, letter in enumerate(self.current_guess):
                arcade.draw_text(
                    letter,
                    start_x + i * LETTER_GAP,
                    start_y - row * 60,
                    arcade.color.WHITE,
                    LETTER_SIZE,
                    anchor_x="center",
                    anchor_y="center",
                )

        if self.game_over:
            text = {
                "win": "ПОБЕДА 🎉",
                "lose": "ПОРАЖЕНИЕ 😿",
                "draw": "НИЧЬЯ 🤝"
            }[self.game_result]

            arcade.draw_text(
                text,
                self.window.width // 2,
                100,
                arcade.color.YELLOW,
                32,
                anchor_x="center",
            )
