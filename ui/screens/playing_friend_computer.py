import arcade

from logic.word import Word


class PlayFriendComputer(arcade.View):
    def __init__(self, difficulty: str):
        super().__init__()

        # -------- TEXTURES --------
        self.background_tex = arcade.load_texture("data/images/background/background.png")

        self.computer_tex_btn = arcade.load_texture("data/images/button/computer_input_word_btn.png")
        self.friend_tex_btn = arcade.load_texture("data/images/button/manual_input_word_btn.png")
        self.home_btn_tex = arcade.load_texture("data/images/button/home_btn.png")

        self.background_tex_left = arcade.load_texture("data/images/background/blue_shtori_left.jpg")
        self.background_tex_right = arcade.load_texture("data/images/background/blue_shtori_right.jpg")

        self.screen_state = "closed"
        self.left_position = 0.0
        self.right_position = 0.0
        self.animation_speed = 2.0

        self.difficulty = difficulty

        self.buttons_hover = {
            "computer": False,
            "friend": False,
        }
        self.button_rects = {
            "friend": None,
            "computer": None,
        }

        # -------- UI --------
        self.home_rect = None
        self.home_hover = False

        self.next_action = None

        # -------- TRANSITIONS --------
        self.fade_alpha = 0
        self.fade_active = False
        self.fade_mode = None
        self.fade_speed = 600

    def on_show_view(self):
        # Свет включается
        self.fade_alpha = 255
        self.fade_active = True
        self.fade_mode = "on"

        self.screen_state = "closed"
        self.left_position = 0.0
        self.right_position = 0.0

    def on_update(self, delta_time):
        speed = self.animation_speed * delta_time

        if self.screen_state == "opening":
            self.left_position += speed
            self.right_position += speed
            if self.left_position >= 1.0:
                self.left_position = 1.0
                self.right_position = 1.0
                self.screen_state = "opened"

        elif self.screen_state == "closing":
            self.left_position -= speed
            self.right_position -= speed
            if self.left_position <= 0.0:
                self.left_position = 0.0
                self.right_position = 0.0
                self.screen_state = "closed"

                # После закрытия — выключаем свет
                self.fade_active = True
                self.fade_mode = "off"

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

                if self.next_action == "home":
                    from ui.screens.menu_screen import MenuScreen
                    self.window.show_view(MenuScreen())

                elif self.next_action == "computer":
                    from ui.screens.computer_game_screen import ComputerGameScreen
                    word = Word.random_by_difficulty(self.difficulty)
                    self.window.show_view(ComputerGameScreen(difficulty=self.difficulty))

                elif self.next_action == "friend":
                    from ui.screens.friend_word_input_screen import FriendWordInputScreen
                    self.window.show_view(FriendWordInputScreen())

    def on_draw(self):
        self.clear()

        scale = self.height / self.background_tex.height
        back_width = self.background_tex.width * scale

        arcade.draw_texture_rect(self.background_tex,
                                 arcade.rect.XYWH(
                                     self.width / 2,
                                     self.height / 2,
                                     back_width,
                                     self.height))

        center_x = self.width / 2
        center_y = self.height / 2

        btn_height = self.height / 10 * 0.8

        scale_shtori = self.height / self.background_tex_left.height
        width = self.background_tex_left.width * scale_shtori

        left_x = center_x - width / 2 - width * self.left_position
        right_x = center_x + width / 2 + width * self.right_position

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
        btn_height = self.height / 10
        y = self.height / 1.8

        buttons = [
            (self.friend_tex_btn, "friend", self.width / 4),
            (self.computer_tex_btn, "computer", self.width * 3 / 4),
        ]

        for texture, name, x in buttons:
            btn_width = texture.width * (btn_height / texture.height)

            rect = arcade.rect.XYWH(x, y, btn_width, btn_height)
            self.button_rects[name] = rect

            arcade.draw_texture_rect(texture, rect)

            if self.buttons_hover[name]:
                arcade.draw_lrbt_rectangle_outline(
                    rect.left,
                    rect.right,
                    rect.bottom,
                    rect.top,
                    arcade.color.YELLOW,
                    3
                )

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

        arcade.draw_texture_rect(self.background_tex_left,
                                 arcade.rect.XYWH(left_x,
                                                  center_y,
                                                  width,
                                                  self.height))

        arcade.draw_texture_rect(self.background_tex_right,
                                 arcade.rect.XYWH(right_x,
                                                  center_y,
                                                  width,
                                                  self.height))
        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(0, self.width, 0, self.height,
                                              (0, 0, 0, int(self.fade_alpha)))

    def on_mouse_motion(self, x, y, dx, dy):
        for key in self.buttons_hover:
            self.buttons_hover[key] = False

        if self.screen_state != "opened":
            return
        # HOME
        self.home_hover = False
        if self.home_rect and self.home_rect.left <= x <= self.home_rect.right \
                and self.home_rect.bottom <= y <= self.home_rect.top:
            self.home_hover = True

        # BUTTONS
        for name, rect in self.button_rects.items():
            if rect and rect.left <= x <= rect.right \
                    and rect.bottom <= y <= rect.top:
                self.buttons_hover[name] = True
            else:
                self.buttons_hover[name] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Первый клик — открываем шторки
        if self.screen_state == "closed":
            self.screen_state = "opening"
            return

        if self.screen_state != "opened":
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.home_hover:
                self.next_action = "home"
                self.fade_active = True
                self.fade_mode = "off"
                self.screen_state = "closing"

            for name in ("computer", "friend"):
                if self.buttons_hover[name]:
                    self.next_action = name
                    self.fade_active = True
                    self.fade_mode = "off"
                    break
        return


    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)