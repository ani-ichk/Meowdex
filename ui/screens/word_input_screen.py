import arcade


class WordInputScreen(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_texture = arcade.load_texture("data/images/background/blue_shtori.jpg")
        self.computer_input_tex = arcade.load_texture("data/images/button/play_btn.png")
        self.user_input_tex = arcade.load_texture("data/images/button/play_btn.png")
        self.exit_btn_tex = arcade.load_texture("data/images/button/exit_btn.png")

        self.robot_rect = None
        self.friend_rect = None
        self.exit_rect = None

        self.fade_mode = None
        self.fade_alpha = 0
        self.fade_active = False
        self.fade_speed = 600

        self.next_action = None

        self.buttons_hover = {
            "robot": False,
            "friend": False,
            "exit": False
        }

        self.buttons_rects = {}

    def on_show_view(self):
        self.fade_alpha = 255
        self.fade_active = True
        self.fade_mode = "on"

    def on_draw(self):
        self.clear()

        scale = self.height / self.background_texture.height
        back_width = self.background_texture.width * scale

        arcade.draw_texture_rect(self.background_texture,
                                 arcade.rect.XYWH(self.width / 2,
                                                  self.height / 2,
                                                  back_width,
                                                  self.height))

        center_x = self.width / 2
        center_y = self.height / 2

        left_limit = self.width * 0.15
        right_limit = self.width * 0.85


        max_button_width = (right_limit - left_limit) / 2 * 0.8
        btn_height = self.height / 10

        robot_scale = min(
            max_button_width / self.computer_input_tex.width,
            btn_height / self.computer_input_tex.height
        )

        robot_w = self.computer_input_tex.width * robot_scale
        robot_h = self.computer_input_tex.height * robot_scale

        self.robot_rect = arcade.rect.XYWH(
            center_x - max_button_width / 2,
            center_y,
            robot_w,
            robot_h
        )

        arcade.draw_texture_rect(self.computer_input_tex, self.robot_rect)

        for name, rect in self.buttons_rects.items():
            if self.buttons_hover[name]:
                arcade.draw_lrbt_rectangle_outline(
                    rect.left,
                    rect.right,
                    rect.bottom,
                    rect.top,
                    arcade.color.YELLOW,
                    3
                )

        self.buttons_rects["robot"] = self.robot_rect

        friend_scale = min(
            max_button_width / self.user_input_tex.width,
            btn_height / self.user_input_tex.height
        )

        friend_w = self.user_input_tex.width * friend_scale
        friend_h = self.user_input_tex.height * friend_scale

        self.friend_rect = arcade.rect.XYWH(
            center_x + max_button_width / 2,
            center_y,
            friend_w,
            friend_h
        )

        arcade.draw_texture_rect(self.user_input_tex, self.friend_rect)

        for name, rect in self.buttons_rects.items():
            if self.buttons_hover[name]:
                arcade.draw_lrbt_rectangle_outline(
                    rect.left,
                    rect.right,
                    rect.bottom,
                    rect.top,
                    arcade.color.YELLOW,
                    3
                )

        self.buttons_rects["friend"] = self.friend_rect

        exit_height = btn_height * 0.8
        exit_width = self.exit_btn_tex.width * (exit_height / self.exit_btn_tex.height)

        self.exit_rect = arcade.rect.XYWH(center_x,
                                          exit_height,
                                          exit_width,
                                          exit_height)

        arcade.draw_texture_rect(self.exit_btn_tex, self.exit_rect)

        for name, rect in self.buttons_rects.items():
            if self.buttons_hover[name]:
                arcade.draw_lrbt_rectangle_outline(
                    rect.left,
                    rect.right,
                    rect.bottom,
                    rect.top,
                    arcade.color.YELLOW,
                    3
                )

        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(0,
                                              self.width,
                                              0,
                                              self.height,
                                              (0, 0, 0, int(self.fade_alpha)))

        self.buttons_rects["exit"] = self.exit_rect

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

                from ui.screens.menu_screen import MenuScreen
                self.window.show_view(MenuScreen())

                if self.next_action == "menu":
                    from ui.screens.menu_screen import MenuScreen
                    self.window.show_view(MenuScreen())

                elif self.next_action == "single":
                    from ui.screens.game_screen import GameScreen
                    self.window.show_view(GameScreen())

                elif self.next_action == "friend":
                    from ui.screens.friend_word_input_screen import FriendWorldInput
                    self.window.show_view(FriendWorldInput())

    def on_mouse_motion(self, x, y, dx, dy):
        for key in self.buttons_hover:
            self.buttons_hover[key] = False

        for name, rect in self.buttons_rects.items():
            if rect.left <= x <= rect.right and rect.bottom <= y <= rect.top:
                self.buttons_hover[name] = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT or self.fade_active:
            return

        if self.buttons_hover["exit"]:
            self.next_action = "menu"
            self.fade_active = True
            self.fade_mode = "off"
            return

        if self.buttons_hover["friend"]:
            self.next_action = "single"
            self.fade_active = True
            self.fade_mode = "off"
            return

        if self.buttons_hover["robot"]:
            self.next_action = "friend"
            self.fade_active = True
            self.fade_mode = "off"
            return

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)
