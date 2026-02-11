import arcade
from ui.screens.friend_game_screen import FriendGameScreen


class FriendWordInputScreen(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_tex = arcade.load_texture(
            "data/images/background/background.png"
        )
        self.home_btn_tex = arcade.load_texture("data/images/button/home_btn.png")

        self.stage = 1  # 1 — вводит игрок 1, 2 — игрок 2
        self.word_p1 = ""
        self.word_p2 = ""
        self.current_input = ""



        self.home_rect = None
        self.home_hover = False
        self.next_action = None

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

                if self.next_action == "menu":
                    from ui.screens.menu_screen import MenuScreen
                    self.window.show_view(MenuScreen())

    def on_draw(self):
        self.clear()

        scale = self.height / self.background_tex.height
        arcade.draw_texture_rect(
            self.background_tex,
            arcade.rect.XYWH(
                self.width / 2,
                self.height / 2,
                self.background_tex.width * scale,
                self.height
            )
        )

        arcade.draw_text(
            f"Игрок {self.stage}, введите слово",
            self.width / 2,
            self.height / 2 + 80,
            arcade.color.WHITE,
            30,
            anchor_x="center"
        )

        # скрытый ввод
        hidden = "*" * len(self.current_input)
        arcade.draw_text(
            hidden,
            self.width / 2,
            self.height / 2,
            arcade.color.YELLOW,
            40,
            anchor_x="center"
        )

        # ----- HOME BUTTON -----
        self.home_rect = arcade.rect.XYWH(
            self.width / 2,
            self.home_btn_tex.height * 2,
            self.home_btn_tex.width,
            self.home_btn_tex.height
        )

        arcade.draw_texture_rect(self.home_btn_tex, self.home_rect)

        if self.home_hover:
            arcade.draw_lrbt_rectangle_outline(
                self.home_rect.left,
                self.home_rect.right,
                self.home_rect.bottom,
                self.home_rect.top,
                arcade.color.YELLOW,
                3
            )

        # ----- FADE -----
        if self.fade_active:
            arcade.draw_lrbt_rectangle_filled(
                0, self.width, 0, self.height,
                (0, 0, 0, int(self.fade_alpha))
            )


    def on_text(self, text):
        if not text.isalpha():
            return

        letter = text.upper()
        if not ("А" <= letter <= "Я" or letter == "Ё"):
            return

        self.current_input += letter

    def on_mouse_motion(self, x, y, dx, dy):
        self.home_hover = False
        if self.home_rect:
            if self.home_rect.left <= x <= self.home_rect.right and \
                    self.home_rect.bottom <= y <= self.home_rect.top:
                self.home_hover = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.home_hover:
            self.next_action = "menu"
            self.fade_active = True
            self.fade_mode = "off"

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            self.current_input = self.current_input[:-1]

        elif key == arcade.key.ENTER:
            if not self.current_input:
                return

            if self.stage == 1:
                self.word_p1 = self.current_input
                self.current_input = ""
                self.stage = 2

            elif self.stage == 2:
                self.word_p2 = self.current_input
                self.window.show_view(
                    FriendGameScreen(self.word_p1, self.word_p2)
                )

        elif key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
