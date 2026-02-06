# Правила игры
import arcade

class Rules(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_texture = arcade.load_texture("data/images/background/background.png")
        self.home_btn_tex = arcade.load_texture("data/images/button/home_btn.png")

        self.home_rect = None
        self.home_hover = False
        self.fade_mode = None
        self.fade_alpha = 0
        self.fade_active = False
        self.fade_speed = 600

    def on_draw(self):
        self.clear()

        # фон
        arcade.draw_texture_rect(
            self.background_texture,
            arcade.rect.XYWH(self.width / 2,
                             self.height / 2,
                             self.width,
                             self.height
                             )
        )

        # затемнение
        arcade.draw_lrbt_rectangle_filled(
            0, self.width, 0, self.height,
            (0, 0, 0, 150)
        )

        # панель
        arcade.draw_lrbt_rectangle_filled(
            self.width * 0.15,
            self.width * 0.85,
            self.height * 0.2,
            self.height * 0.8,
            (30, 30, 30, 220)
        )

        arcade.draw_lrbt_rectangle_outline(
            self.width * 0.15,
            self.width * 0.85,
            self.height * 0.2,
            self.height * 0.8,
            arcade.color.WHITE,
            3
        )

        # текст
        arcade.draw_text(
            "ПРАВИЛА ИГРЫ\n\n"
            "• Угадай слово за ограниченное число попыток\n"
            "• Ошибки приближают поражение\n"
            "• Чем выше сложность — тем больше награда\n"
            "• Угадал с первой попытки — x2 рыбок\n"
            "• Серия побед даёт бонусы",
            self.width * 0.18,
            self.height * 0.75,
            arcade.color.WHITE,
            font_size=20,
            width=self.width * 0.64,
            multiline=True
        )

        btn_height = self.height / 10

        home_height = btn_height * 0.8
        home_width = self.home_btn_tex.width * (home_height / self.home_btn_tex.height)

        self.home_rect = arcade.rect.XYWH(self.width / 2,
                                          home_height,
                                          home_width,
                                          home_height)

        arcade.draw_texture_rect(self.home_btn_tex, self.home_rect)

        if self.home_hover:
            arcade.draw_lrbt_rectangle_outline(self.home_rect.left,
                                               self.home_rect.right,
                                               self.home_rect.bottom,
                                               self.home_rect.top,
                                               arcade.color.YELLOW,
                                               3)
    def on_update(self, delta_time):
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

    def on_mouse_motion(self, x, y, dx, dy):
        self.home_hover = False
        if self.home_rect:
            if (self.home_rect.left <= x <= self.home_rect.right and
                    self.home_rect.bottom <= y <= self.home_rect.top):
                self.home_hover = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.home_hover and not self.fade_active:
                self.fade_active = True
                self.fade_mode = "off"
        return

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)




