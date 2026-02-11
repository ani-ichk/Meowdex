import arcade


class Rules(arcade.View):
    def __init__(self):
        super().__init__()

        self.home_btn_tex = arcade.load_texture("data/images/button/home_btn.png")

        self.background_tex_left = arcade.load_texture("data/images/background/blue_shtori_left.jpg")
        self.background_tex_right = arcade.load_texture("data/images/background/blue_shtori_right.jpg")

        self.pashalka_tex = arcade.load_texture("data/images/background/pashalochka.png")

        self.panel_tex = arcade.load_texture("data/images/label/rules_grid.png")

        self.home_rect = None
        self.home_hover = False

        self.screen_state = "closed"
        self.left_position = 0.0
        self.right_position = 0.0
        self.animation_speed = 2.0

        self.fade_alpha = 0
        self.fade_active = False
        self.fade_mode = None
        self.fade_speed = 600

        self.world_offset_x = 0
        self.move_speed = 300

        self.move_left = False
        self.move_right = False

        self.max_offset = (
            self.background_tex_left.width
            + self.pashalka_tex.width * 2
        )

    def on_show_view(self):
        self.fade_alpha = 255
        self.fade_active = True
        self.fade_mode = "on"

        self.screen_state = "closed"
        self.left_position = 0.0
        self.right_position = 0.0

        self.world_offset_x = 0
        self.move_left = False
        self.move_right = False

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

                self.fade_active = True
                self.fade_mode = "off"

        if self.screen_state == "opened":
            if self.move_left:
                self.world_offset_x += self.move_speed * delta_time
                if self.world_offset_x > self.max_offset:
                    self.world_offset_x = self.max_offset

            if self.move_right:
                self.world_offset_x -= self.move_speed * delta_time
                if self.world_offset_x < 0:
                    self.world_offset_x = 0

        if self.fade_active:
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

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.panel_tex,
            arcade.rect.XYWH(
                self.width / 2 + self.world_offset_x,
                self.height / 2,
                self.panel_tex.width * (self.height / self.panel_tex.height),
                self.height * 0.6
            )
        )

        arcade.draw_texture_rect(
            self.pashalka_tex,
            arcade.rect.XYWH(
                self.width / 2
                - self.background_tex_left.width
                - self.pashalka_tex.width * 2
                + self.world_offset_x,
                self.height / 2,
                self.pashalka_tex.width,
                self.height * 0.6
            )
        )

        arcade.draw_text(
            "ПРАВИЛА ИГРЫ\n\n"
            "• Одиночный режим:\n"
            "   • Угадай слово за ограниченное число попыток\n"
            "   • За выигрыш идет награда\n"
            "   • Чем выше уровень сложности — тем выше награда\n"
            "   • Угадал с первой попытки — x2 рыбок\n"
            "\n"
            "Режим с другом\n"
            "Ввод слов идет поочереди, левый игрок вводит слово для правого игрока и наоборот\n"
            "Если один из игроков угадал слово раньше чем у него закончились попытки, ждем второго игрока\n",
            self.width * 0.18 + self.world_offset_x,
            self.height * 0.7,
            arcade.color.WHITE,
            align="left",
            font_name=("Pixeloid Sans", "arial"),
            font_size=22,
            width=self.width * 0.64,
            multiline=True
        )

        btn_height = self.height / 10
        home_height = btn_height * 0.8
        home_width = self.home_btn_tex.width * (home_height / self.home_btn_tex.height)

        self.home_rect = arcade.rect.XYWH(
            self.width / 2 + self.world_offset_x,
            home_height,
            home_width,
            home_height
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

        width = self.background_tex_left.width * self.height / self.background_tex_left.height
        center_y = self.height / 2

        left_x = self.width / 2 - width / 2 - width * self.left_position
        right_x = self.width / 2 + width / 2 + width * self.right_position

        arcade.draw_texture_rect(
            self.background_tex_left,
            arcade.rect.XYWH(left_x, center_y, width, self.height)
        )

        arcade.draw_texture_rect(
            self.background_tex_right,
            arcade.rect.XYWH(right_x, center_y, width, self.height)
        )

        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(
                0, self.width, 0, self.height,
                (0, 0, 0, int(self.fade_alpha))
            )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)

        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)

        elif key == arcade.key.LEFT:
            self.move_left = True
        elif key == arcade.key.RIGHT:
            self.move_right = True

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.move_left = False
        elif key == arcade.key.RIGHT:
            self.move_right = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.home_hover = False
        if self.home_rect:
            if self.home_rect.left <= x <= self.home_rect.right and \
               self.home_rect.bottom <= y <= self.home_rect.top:
                self.home_hover = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        if self.screen_state == "closed":
            self.screen_state = "opening"
            return

        if self.screen_state != "opened":
            return

        if self.home_hover:
            self.screen_state = "closing"