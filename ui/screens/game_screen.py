import arcade


class GameScreen(arcade.View):
    def __init__(self, word):
        super().__init__()

        self.target_word = str(word).lower()
        self.input_word = ""

        self.title = arcade.Text(
            "Угадайте слово",
            400, 520,
            anchor_x="center",
            font_size=28
        )

        self.input_text = arcade.Text(
            "",
            400, 360,
            anchor_x="center",
            font_size=36,
            color=arcade.color.YELLOW
        )

    def on_draw(self):
        self.clear()

        self.title.draw()
        self.input_text.text = self.input_word
        self.input_text.draw()

    def on_text(self, text):
        self.input_word += text.lower()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            self.input_word = self.input_word[:-1]

        elif key == arcade.key.ENTER:
            print("Введено:", self.input_word)
            print("Загадано:", self.target_word)
