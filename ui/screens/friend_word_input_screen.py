import arcade
from models.word import Word


class FriendWordInputScreen(arcade.View):
    def __init__(self, difficulty):
        super().__init__()

        self.difficulty = difficulty

        self.background_texture = arcade.load_texture(
            "data/images/background/blue_shtori.jpg"
        )

        self.input_word = ""

        self.fade_alpha = 0
        self.fade_active = False
        self.fade_mode = None
        self.fade_speed = 600

    def on_show_view(self):
        self.fade_alpha = 255
        self.fade_active = True
        self.fade_mode = "on"

    def on_update(self, delta_time):
        if not self.fade_active:
            return

        if self.fade_mode == "on":
            self.fade_alpha -= self.fade_speed * delta_time
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_active = False
                self.fade_mode = None

        elif self.fade_mode == "off":
            self.fade_alpha += self.fade_speed * delta_time
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.fade_active = False

                from ui.screens.game_screen import GameScreen
                self.window.show_view(
                    GameScreen(
                        Word(self.input_word),
                        mode="friend",
                        difficulty=self.difficulty
                    )
                )

    def on_key_press(self, key, modifiers):
        if self.fade_active:
            return

        if arcade.key.A <= key <= arcade.key.Z:
            self.input_word += chr(key).lower()

        elif key == arcade.key.BACKSPACE:
            self.input_word = self.input_word[:-1]

        elif key == arcade.key.ENTER:
            if len(self.input_word) > 0:
                self.fade_active = True
                self.fade_mode = "off"

        elif key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)

    def on_draw(self):
        self.clear()

        scale = self.height / self.background_texture.height
        back_width = self.background_texture.width * scale

        arcade.draw_texture_rect(
            self.background_texture,
            arcade.rect.XYWH(
                self.width / 2,
                self.height / 2,
                back_width,
                self.height
            )
        )

        center_x = self.width / 2

        arcade.draw_text(
            "Друг, введи слово",
            center_x,
            self.height * 0.6,
            arcade.color.WHITE,
            32,
            anchor_x="center"
        )

        arcade.draw_text(
            "*" * len(self.input_word),
            center_x,
            self.height * 0.5,
            arcade.color.YELLOW,
            40,
            anchor_x="center"
        )

        arcade.draw_text(
            "ENTER — начать игру",
            center_x,
            self.height * 0.4,
            arcade.color.LIGHT_GRAY,
            18,
            anchor_x="center"
        )

        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(
                0,
                self.width,
                0,
                self.height,
                (0, 0, 0, int(self.fade_alpha))
            )