# Правила игры
import arcade


class Rules(arcade.View):
    def __init__(self):
        super().__init__()

        self.home_btn_tex = arcade.load_texture("data/images/button/home_btn.png")

        self.background_tex_left = arcade.load_texture("data/images/background/blue_shtori_left.jpg")
        self.background_tex_right = arcade.load_texture("data/images/background/blue_shtori_right.jpg")

        self.panel_tex = arcade.load_texture("data/images/label/rules_grid.png")

        self.home_rect = None
        self.home_hover = False

        # --- ЛОГИКА ШТОРОК ---
        self.screen_state = "closed"
        self.left_position = 0.0
        self.right_position = 0.0
        self.animation_speed = 2.0

        # --- ЛОГИКА СВЕТА ---
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

        # ---------- ШТОРКИ ----------
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

        # ---------- СВЕТ ----------
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

        scale = self.height / self.panel_tex.height

        arcade.draw_texture_rect(
            self.panel_tex,
            arcade.rect.XYWH(
                self.width / 2,
                self.height / 2,
                self.panel_tex.width * scale,
                self.height * 0.6
            )
        )

        # текст
        arcade.draw_text(
            "ПРАВИЛА ИГРЫ\n\n"
            "• Угадай слово за ограниченное число попыток\n"
            "• За выигрыш идет награда\n"
            "• Чем выше уровень сложности — тем выше награда\n"
            "• Угадал с первой попытки — x2 рыбок\n",
            self.width * 0.18,
            self.height * 0.6,
            arcade.color.WHITE,
            align = "left",
            font_name=("Pixeloid Sans", "arial"),
            font_size=30,
            width=self.width * 0.64,
            multiline=True
        )

        # кнопка домой
        btn_height = self.height / 10
        home_height = btn_height * 0.8
        home_width = self.home_btn_tex.width * (home_height / self.home_btn_tex.height)

        self.home_rect = arcade.rect.XYWH(
            self.width / 2,
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

        # шторки
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

        # затемнение
        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(
                0, self.width, 0, self.height,
                (0, 0, 0, int(self.fade_alpha))
            )

    def on_mouse_motion(self, x, y, dx, dy):
        self.home_hover = False
        if self.home_rect:
            if self.home_rect.left <= x <= self.home_rect.right and \
               self.home_rect.bottom <= y <= self.home_rect.top:
                self.home_hover = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Первый клик — открываем шторки (как в PlayScreen)
        if self.screen_state == "closed":
            self.screen_state = "opening"
            return

        if self.screen_state != "opened":
            return

        if self.home_hover:
            self.screen_state = "closing"

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)