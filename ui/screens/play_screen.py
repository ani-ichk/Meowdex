import arcade
from logic.word import Word
from logic.difficulty import EASY, MEDIUM, NORMAL, HARD, EXPERT


DIFFICULTY_MAP = {
    "easy": EASY,
    "normal": NORMAL,
    "hard": HARD
}


class PlayScreen(arcade.View):
    def __init__(self):
        super().__init__()

        self.background_tex = arcade.load_texture("data/images/background/background.png")
        self.singleplayer_label_tex = arcade.load_texture("data/images/label/single_mod.png")
        self.with_friend_label_tex = arcade.load_texture("data/images/label/friend_mod.png")

        self.easy_btn_tex = arcade.load_texture("data/images/button/easy_btn.png")
        self.medium_btn_tex = arcade.load_texture("data/images/button/medium_btn.png")
        self.hard_btn_tex = arcade.load_texture("data/images/button/hard_btn.png")
        self.expert_btn_tex = arcade.load_texture("data/images/button/expert_btn.png")

        self.exit_btn_tex = arcade.load_texture("data/images/button/exit_btn.png")

        self.background_tex_left = arcade.load_texture("data/images/background/blue_shtori_left.jpg")
        self.background_tex_right = arcade.load_texture("data/images/background/blue_shtori_right.jpg")

        self.screen_state = "closed"
        self.left_position = 0.0
        self.right_position = 0.0
        self.animation_speed = 2.0

        self.fade_alpha = 0
        self.fade_active = False
        self.fade_mode = None
        self.fade_speed = 600

        self.selected_difficulty = None

        self.next_action = None

        self.buttons_hover = {
            "single_easy": False,
            "single_medium": False,
            "single_hard": False,
            "single_expert": False,
            "friend_easy": False,
            "friend_medium": False,
            "friend_hard": False,
            "exit": False
        }

        self.buttons_rects = {}

    def on_show_view(self):
        # Свет включается
        self.fade_alpha = 255
        self.fade_active = True
        self.fade_mode = "on"

        self.screen_state = "closed"
        self.left_position = 0.0
        self.right_position = 0.0
        self.next_action = None

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

                    elif self.next_action == "single":
                        from ui.screens.game_screen import GameScreen
                        word = Word.random_by_difficulty(self.selected_difficulty)
                        self.window.show_view(GameScreen(
                            target_word=word.value,
                            difficulty=self.selected_difficulty))



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
        spacing = btn_height * 1.2

        scale_shtori = self.height / self.background_tex_left.height
        width = self.background_tex_left.width * scale_shtori

        left_center_x = center_x - width / 2 + btn_height
        right_center_x = center_x + width / 2 - btn_height

        label_height = self.singleplayer_label_tex.height * scale * 0.7
        label_y = self.height * 5 / 6
        label_w = self.singleplayer_label_tex.width * scale * 0.7

        arcade.draw_texture_rect(self.singleplayer_label_tex,
                                 arcade.rect.XYWH(left_center_x,
                                                  label_y,
                                                  label_w,
                                                  label_height))

        arcade.draw_texture_rect(self.with_friend_label_tex,
                                 arcade.rect.XYWH(right_center_x,
                                                  label_y,
                                                  label_w,
                                                  label_height))

        self.buttons_rects.clear()

        single_buttons = [
            (self.easy_btn_tex, "single_easy"),
            (self.medium_btn_tex, "single_medium"),
            (self.hard_btn_tex, "single_hard"),
            (self.expert_btn_tex, "single_expert"),
        ]
        start_y = center_y + spacing * 2
        for i, (texture, name) in enumerate(single_buttons):
            btn_width = texture.width * (btn_height / texture.height)
            y = start_y - i * spacing

            rect = arcade.rect.XYWH(left_center_x, y, btn_width, btn_height)
            self.buttons_rects[name] = rect

            arcade.draw_texture_rect(texture, rect)

            if self.buttons_hover[name]:
                arcade.draw_lrbt_rectangle_outline(rect.left,
                                                   rect.right,
                                                   rect.bottom,
                                                   rect.top,
                                                   arcade.color.YELLOW,
                                                   3)

        friend_buttons = [
            (self.easy_btn_tex, "friend_easy"),
            (self.medium_btn_tex, "friend_medium"),
        ]

        for i, (texture, name) in enumerate(friend_buttons):
            btn_width = texture.width * (btn_height / texture.height)
            y = start_y - i * spacing

            rect = arcade.rect.XYWH(right_center_x, y, btn_width, btn_height)
            self.buttons_rects[name] = rect

            arcade.draw_texture_rect(texture, rect)

            if self.buttons_hover[name]:
                arcade.draw_lrbt_rectangle_outline(rect.left,
                                                   rect.right,
                                                   rect.bottom,
                                                   rect.top,
                                                   arcade.color.YELLOW,
                                                   3)

        exit_height = btn_height * 0.8
        exit_width = self.exit_btn_tex.width * (exit_height / self.exit_btn_tex.height)

        exit_rect = arcade.rect.XYWH(center_x, exit_height, exit_width, exit_height)
        self.buttons_rects["exit"] = exit_rect

        arcade.draw_texture_rect(self.exit_btn_tex,
                                 exit_rect)

        if self.buttons_hover["exit"]:
            arcade.draw_lrbt_rectangle_outline(exit_rect.left,
                                               exit_rect.right,
                                               exit_rect.bottom,
                                               exit_rect.top,
                                               arcade.color.YELLOW,
                                               3)

        left_x = center_x - width / 2 - width * self.left_position
        right_x = center_x + width / 2 + width * self.right_position

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

        for name, rect in self.buttons_rects.items():
            if rect.left <= x <= rect.right and rect.bottom <= y <= rect.top:
                self.buttons_hover[name] = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Первый клик — открываем шторки
        if self.screen_state == "closed":
            self.screen_state = "opening"
            return

        if self.screen_state != "opened":
            return

        if self.buttons_hover["exit"]:
            self.next_action = "menu"
            self.screen_state = "closing"
            return

        for name in self.buttons_hover:
            if self.buttons_hover[name] and name != "exit":

                if name.startswith("single_easy"):
                    self.selected_difficulty = EASY
                    self.next_action = "single"

                elif name.startswith("single_medium"):
                    self.selected_difficulty = MEDIUM
                    self.next_action = "single"

                elif name.startswith("single_hard"):
                    self.selected_difficulty = HARD
                    self.next_action = "single"

                elif name.startswith("single_expert"):
                    self.selected_difficulty = EXPERT
                    self.next_action = "single"

                elif name.startswith("friend_easy"):
                    self.selected_difficulty = "easy"
                    self.next_action = "friend"

                elif name.startswith("friend_hard"):
                    self.selected_difficulty = "hard"
                    self.next_action = "friend"

                else:
                    return

                self.screen_state = "closing"
                return

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)