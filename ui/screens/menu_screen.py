import arcade


class MenuScreen(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_texture = arcade.load_texture("data/images/background/blue_shtori.jpg")
        self.logo_texture = arcade.load_texture("data/images/logo/logo.png")
        self.play_btn_texture = arcade.load_texture("data/images/button/play_btn.png")
        self.progress_btn_texture = arcade.load_texture("data/images/button/progress_btn.png")
        self.exit_btn_texture = arcade.load_texture("data/images/button/exit_btn.png")
        self.instructions_btn_texture = arcade.load_texture("data/images/button/home_btn.png") # UPDATE

        self.buttons_hover = {
            "play": False,
            "progress": False,
            "instructions": False,
            "exit": False
        }

        self.logo_start_y = None
        self.logo_target_y = None
        self.logo_current_y = None

        self.logo_animating = True
        self.logo_anim_time = 0.0
        self.logo_anim_duration = 0.6

        self.fade_mode = None
        self.fade_alpha = 0
        self.fade_active = False
        self.fade_speed = 600

        self.next_action = None

    def on_show_view(self):
        self.logo_animating = True
        self.logo_anim_time = 0.0

        self.logo_start_y = self.height + self.height / 3
        self.logo_target_y = self.height - (self.height / 6)
        self.logo_current_y = self.logo_start_y

        self.fade_alpha = 255
        self.fade_active = True
        self.fade_mode = "on"

    def on_resize(self, width: int, height: int):
        super().on_resize(width, height)

        self.logo_target_y = height - (height / 6)
        self.logo_current_y = height - (height / 6)

    def on_draw(self):
        self.clear()

        scale = self.height / self.background_texture.height
        back_width = self.background_texture.width * scale

        arcade.draw_texture_rect(self.background_texture,
                                 arcade.rect.XYWH(
                                     self.width / 2,
                                     self.height / 2,
                                     back_width,
                                     self.height))

        logo_height = self.height / 3
        logo_width = self.logo_texture.width * (logo_height / self.logo_texture.height)

        arcade.draw_texture_rect(self.logo_texture,
                                 arcade.rect.XYWH(self.width / 2,
                                                  self.logo_current_y,
                                                  logo_width,
                                                  logo_height))

        btn_height = self.height / 10
        start_y = self.height / 1.8
        spacing = btn_height * 1.2

        buttons = [
            (self.play_btn_texture, "play"),
            (self.progress_btn_texture, "progress"),
            (self.instructions_btn_texture, "instructions"),
            (self.exit_btn_texture, "exit"),
        ]

        for i, (texture, name) in enumerate(buttons):
            btn_width = texture.width * (btn_height / texture.height)
            y = start_y - i * spacing

            arcade.draw_texture_rect(texture,
                                     arcade.rect.XYWH(self.width / 2,
                                                      y,
                                                      btn_width,
                                                      btn_height))

            # Выделение кнопки при наведении
            if self.buttons_hover[name]:
                arcade.draw_lrbt_rectangle_outline(self.width / 2 - btn_width / 2,
                                                   self.width / 2 + btn_width / 2,
                                                   y - btn_height / 2,
                                                   y + btn_height / 2,
                                                   arcade.color.YELLOW,
                                                   3)

        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(0,
                                              self.width,
                                              0,
                                              self.height,
                                              (0, 0, 0, int(self.fade_alpha)))

    def on_update(self, delta_time):
        if self.logo_animating:
            self.logo_anim_time += delta_time
            progress = self.logo_anim_time / self.logo_anim_duration
            progress = min(progress, 1.0)
            self.logo_current_y = ((1 - progress) * self.logo_start_y + progress * self.logo_target_y)
            if progress >= 1.0:
                self.logo_animating = False

        if self.fade_active:
            if self.fade_mode == "off":
                self.fade_alpha += self.fade_speed * delta_time
                if self.fade_alpha >= 255:
                    self.fade_alpha = 255
                    self.fade_active = False
                    if self.next_action == "play":
                        from ui.screens.play_screen import PlayScreen
                        self.window.show_view(PlayScreen())
                    elif self.next_action == "progress":
                        from ui.screens.progress_screen import ProgressScreen
                        self.window.show_view(ProgressScreen())
                    elif self.next_action == "instructions":
                        from ui.screens.rules_game_screen import Rules
                        self.window.show_view(Rules())
            elif self.fade_mode == "on":
                self.fade_alpha -= self.fade_speed * delta_time
                if self.fade_alpha <= 0:
                    self.fade_alpha = 0
                    self.fade_active = False
                    self.fade_mode = None

    def on_mouse_motion(self, x, y, dx, dy):
        btn_height = self.height / 10
        start_y = self.height / 1.8
        spacing = btn_height * 1.2

        for i, name in enumerate(list(self.buttons_hover.keys())):
            btn_y = start_y - i * spacing
            half_h = btn_height / 2
            self.buttons_hover[name] = (self.width / 2 - 150 < x < self.width / 2 + 150
                                        and btn_y - half_h < y < btn_y + half_h)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.buttons_hover["exit"]:
                self.window.close()
            for name in ("play", "progress", "instructions"):
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