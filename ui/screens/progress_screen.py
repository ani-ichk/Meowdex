import arcade
from models.progress import Progress


class ProgressScreen(arcade.View):
    def __init__(self):
        super().__init__()

        self.progress = Progress()

        self.background_texture = arcade.load_texture("data/images/background/blue_shtori.jpg")
        self.icon_rank_1_tex = arcade.load_texture("data/images/label/rank_1.png")

        self.fish_texture = arcade.load_texture("data/images/label/fish_game.png")

        self.current_rank_1_tex = arcade.load_texture("data/images/label/current_rank_1.png")
        self.current_rank_2_tex = arcade.load_texture("data/images/label/current_rank_2.png")
        self.current_rank_3_tex = arcade.load_texture("data/images/label/current_rank_3.png")
        # self.current_rank_4_tex = arcade.load_texture("data/images/label/current_rank_4.png")
        # self.current_rank_5_tex = arcade.load_texture("data/images/label/current_rank_5.png")
        # self.current_rank_6_tex = arcade.load_texture("data/images/label/current_rank_6.png")
        # self.current_rank_7_tex = arcade.load_texture("data/images/label/current_rank_7.png")
        # self.current_rank_8_tex = arcade.load_texture("data/images/label/current_rank_8.png")
        # self.current_rank_9_tex = arcade.load_texture("data/images/label/current_rank_9.png")
        # self.current_rank_10_tex = arcade.load_texture("data/images/label/current_rank_10.png")

        self.next_rank_2_tex = arcade.load_texture("data/images/label/next_rank_2.png")
        self.next_rank_3_tex = arcade.load_texture("data/images/label/next_rank_3.png")
        # self.next_rank_4_tex = arcade.load_texture("data/images/label/next_rank_4.png")
        # self.next_rank_5_tex = arcade.load_texture("data/images/label/next_rank_5.png")
        # self.next_rank_6_tex = arcade.load_texture("data/images/label/next_rank_6.png")
        # self.next_rank_7_tex = arcade.load_texture("data/images/label/next_rank_7.png")
        # self.next_rank_8_tex = arcade.load_texture("data/images/label/next_rank_8.png")
        # self.next_rank_9_tex = arcade.load_texture("data/images/label/next_rank_9.png")
        # self.next_rank_10_tex = arcade.load_texture("data/images/label/next_rank_10.png")

        self.win_streak_tex = arcade.load_texture("data/images/label/win_streak.png")

        self.exit_btn_tex = arcade.load_texture("data/images/button/exit_btn.png")

        self.exit_rect = None
        self.exit_hover = False

        self.fade_mode = None
        self.fade_alpha = 0
        self.fade_active = False
        self.fade_speed = 600

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

        icon_x = self.width / 2 - self.width * 0.15
        icon_y = self.height / 2 + self.height * 0.25

        icon_height = self.height * 0.2
        icon_width = self.icon_rank_1_tex.width * (icon_height / self.icon_rank_1_tex.height)

        icon_rect = arcade.rect.XYWH(icon_x,
                                     icon_y,
                                     icon_width,
                                     icon_height)

        arcade.draw_texture_rect(self.icon_rank_1_tex, icon_rect)

        # if 0 < self.player.fish < 20:
        current_rank = self.progress.current_rank()

        current_rank_tex = {
            1: self.current_rank_1_tex,
            2: self.current_rank_2_tex,
            3: self.current_rank_3_tex,
        }.get(current_rank, self.current_rank_1_tex)

        arcade.draw_texture_rect(current_rank_tex,
                                 arcade.rect.XYWH(self.width / 2 + 0.2 + current_rank_tex.width / 2,
                                                  self.height / 2 + self.height * 0.25,
                                                  current_rank_tex.width * scale,
                                                  current_rank_tex.height * scale))

        next_rank = self.progress.next_rank()

        next_rank_tex = {
            2: self.next_rank_2_tex,
            3: self.next_rank_3_tex,
        }.get(next_rank, self.next_rank_2_tex)

        arcade.draw_texture_rect(next_rank_tex,
                                 arcade.rect.XYWH(
                                     self.width / 2, self.height / 2,
                                     next_rank_tex.width * scale,
                                     next_rank_tex.height * scale))

        fish_current = self.progress.fish_progress_in_rank()
        fish_needed = self.progress.next_rank_requirement()

        text_x = self.width / 2 - 70
        text_y = self.height / 2 - self.next_rank_2_tex.height * scale * 0.3

        arcade.draw_text(
            f"{fish_current} / {fish_needed}",
            text_x,
            text_y,
            arcade.color.WHITE,
            font_size=22,
            anchor_x="left",
            anchor_y="center"
        )

        arcade.draw_texture_rect(
            self.fish_texture,
            arcade.rect.XYWH(
                text_x + 120,
                text_y,
                self.fish_texture.width * scale * 0.1,
                self.fish_texture.height * scale * 0.1
            )
        )

        arcade.draw_texture_rect(self.win_streak_tex,
                                 arcade.rect.XYWH(self.width / 2,
                                                  self.height / 2 - self.next_rank_2_tex.height * scale / 2 -
                                                  self.win_streak_tex.height * scale / 2 * 1.2,
                                                  self.win_streak_tex.width * scale,
                                                  self.win_streak_tex.height * scale))

        streak_value = self.progress.win_streak

        text_x = self.width / 2 + self.win_streak_tex.width * scale / 2 - 80
        text_y = self.height / 2 - self.next_rank_2_tex.height * scale / 2 - \
                 self.win_streak_tex.height * scale / 2 * 1.2

        arcade.draw_text(
            str(streak_value),
            text_x,
            text_y,
            arcade.color.WHITE,
            font_size=33,
            anchor_x="left",
            anchor_y="center"
        )

        center_x = self.width / 2
        btn_height = self.height / 10

        exit_height = btn_height * 0.8
        exit_width = self.exit_btn_tex.width * (exit_height / self.exit_btn_tex.height)

        self.exit_rect = arcade.rect.XYWH(center_x,
                                          exit_height,
                                          exit_width,
                                          exit_height)

        arcade.draw_texture_rect(self.exit_btn_tex, self.exit_rect)

        if self.exit_hover:
            arcade.draw_lrbt_rectangle_outline(self.exit_rect.left,
                                               self.exit_rect.right,
                                               self.exit_rect.bottom,
                                               self.exit_rect.top,
                                               arcade.color.YELLOW,
                                               3)

        if self.fade_alpha > 0:
            arcade.draw_lrbt_rectangle_filled(0,
                                              self.width,
                                              0,
                                              self.height,
                                              (0, 0, 0, int(self.fade_alpha)))

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

    def on_mouse_motion(self, x, y, dx, dy):
        self.exit_hover = False
        if self.exit_rect:
            if (self.exit_rect.left <= x <= self.exit_rect.right and
                    self.exit_rect.bottom <= y <= self.exit_rect.top):
                self.exit_hover = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.exit_hover and not self.fade_active:
                self.fade_active = True
                self.fade_mode = "off"
        return

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)
