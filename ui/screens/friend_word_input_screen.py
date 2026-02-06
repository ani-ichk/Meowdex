import arcade


class FriendWordInputScreen(arcade.View):
    def __init__(self):
        super().__init__()
        self.input_word = ""

        self.text = arcade.Text(
            "Введите слово для соперника",
            400, 500,
            anchor_x="center",
            font_size=28
        )

        self.input_text = arcade.Text(
            "",
            400, 350,
            anchor_x="center",
            font_size=36,
            color=arcade.color.YELLOW
        )

    def on_draw(self):
        self.clear()

        arcade.draw_text(
            "ВВЕДИ СЛОВО ДЛЯ ДРУГА",
            self.window.width // 2,
            self.window.height - 100,
            arcade.color.WHITE,
            28,
            anchor_x="center"
        )

        # МАСКА ВМЕСТО БУКВ
        masked = "●" * len(self.input_word)

        arcade.draw_text(
            masked,
            self.window.width // 2,
            self.window.height // 2,
            arcade.color.YELLOW,
            36,
            anchor_x="center"
        )

    def on_text(self, text):
        self.input_word += text.lower()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            self.input_word = self.input_word[:-1]

        elif key == arcade.key.ENTER and self.input_word:
            from ui.screens.game_screen import GameScreen
            self.window.show_view(GameScreen(self.input_word))

