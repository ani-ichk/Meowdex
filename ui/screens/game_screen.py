import arcade
from ui.screens.result_screen import ResultScreen


class GameScreen(arcade.View):
    def __init__(self, target_word: str, difficulty):
        super().__init__()

        self.background_tex = arcade.load_texture("data/images/background/background.png")

        self.background_tex_left = arcade.load_texture("data/images/background/blue_shtori_left.jpg")
        self.background_tex_right = arcade.load_texture("data/images/background/blue_shtori_right.jpg")

        self.grid_3_tex = arcade.load_texture("data/images/grids/grid_3.png")
        self.grid_4_tex = arcade.load_texture("data/images/grids/grid_4.png")
        self.grid_5_tex = arcade.load_texture("data/images/grids/grid_5.png")
        self.grid_6_tex = arcade.load_texture("data/images/grids/grid_6.png")
        self.grid_7_tex = arcade.load_texture("data/images/grids/grid_7.png")
        self.grid_8_tex = arcade.load_texture("data/images/grids/grid_8.png")
        self.grid_9_tex = arcade.load_texture("data/images/grids/grid_9.png")

        self.home_btn_tex = arcade.load_texture("data/images/button/home_btn.png")

        self.background_tex_left = arcade.load_texture("data/images/background/blue_shtori_left.jpg")
        self.background_tex_right = arcade.load_texture("data/images/background/blue_shtori_right.jpg")

        self.target_word = target_word.upper()
        self.difficulty = difficulty

        if self.difficulty == "easy":
            self.attempts_left = 4
        elif self.difficulty == "medium":
            self.attempts_left = 5
        elif self.difficulty == "hard":
            self.attempts_left = 4
        elif self.difficulty == "expert":
            self.attempts_left = 3

        self.current_input = ""
        self.guesses = []

        self.game_res = None

        self.home_rect = None
        self.home_hover = False

        self.next_action = None

        self.screen_state = "closed"
        self.left_position = 0.0
        self.right_position = 0.0
        self.animation_speed = 2.0

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

        if len(self.target_word) == 3 or len(self.target_word) == 4:
            arcade.draw_texture_rect(self.grid_3_tex,
                                     arcade.rect.XYWH(self.width / 2,
                                                      self.height / 4 * 2.5,
                                                      self.grid_3_tex.width * scale * 0.7,
                                                      self.grid_3_tex.height * scale * 0.7))

        self.home_rect = arcade.rect.XYWH(self.width / 2,
                                          self.home_btn_tex.height * 3.3,
                                          self.home_btn_tex.width,
                                          self.home_btn_tex.height)

        arcade.draw_texture_rect(self.home_btn_tex, self.home_rect)

        if self.home_hover:
            arcade.draw_lrbt_rectangle_outline(self.home_rect.left,
                                               self.home_rect.right,
                                               self.home_rect.bottom,
                                               self.home_rect.top,
                                               arcade.color.YELLOW,
                                               3)

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

                    if self.next_action == "menu":
                        from ui.screens.menu_screen import MenuScreen
                        self.window.show_view(MenuScreen())

                    # self.window.show_view(ResultScreen(difficulty=???
                    #                                        attempt=???
                    #                                        game_res=self.game_res (win/loss)))

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
            if self.home_hover:
                self.next_action = "menu"
                self.screen_state = "closing"
                return
        return
    # ---------- INPUT ----------

    # ---------- GAME LOGIC ----------

    # ---------- LETTER CHECK ----------

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)
