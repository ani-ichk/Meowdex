import arcade

# ДОБАВИТЬ БЛЮР НА ЗАДНИЙ ФОН

# открытие/закрытие шторок и включение/выключение света БУКВАЛЬНО как в плэй_скрин:
# когда открывается окно, то:
# - включается свет
# - после этого шторки открываются БЕЗ НАЖАТИЯ просто открываются
# когда нажали на кнопку home_btn:
# - закрыли шторы
# - выключили свет
# - выполняем выход к окну меню

# логика начисления рыбок

# перенести логику progress.py СЮДА
# после переноса логики из progress.py, progress.py удаляется -> поломка в progress_screen.py

class ResultScreen(arcade.View):
    def __init__(self, difficulty, attempt, game_res):
        super().__init__()

        self.background_texture = arcade.load_texture("data/images/background/blue_shtori.jpg")

        self.single_win_tex = arcade.load_texture("data/images/label")
        self.single_loss_tex = arcade.load_texture("data/images/label")
        self.friend_win_tex = arcade.load_texture("data/images/label")
        self.friend_loss_tex = arcade.load_texture("data/images/label")
        self.draw_tex = arcade.load_texture("data/images/label")

        self.home_btn_tex = arcade.load_texture("data/images/button/home_btn.png")

        self.background_tex_left = arcade.load_texture("data/images/background/blue_shtori_left.jpg")
        self.background_tex_right = arcade.load_texture("data/images/background/blue_shtori_right.jpg")

        self.game_res = game_res

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

        scale = self.height / self.single_win_tex.height

        if self.game_res == "win":
            arcade.draw_texture_rect(self.single_win_tex,
                                     arcade.rect.XYWH(self.width / 2,
                                                      self.height / 2,
                                                      self.single_win_tex.width * scale,
                                                      self.height))

            # считаем сколько рыбок начислить и передать в текст
            # в зависимости от СЛОЖНОСТИ, НОМЕРА ПОПЫТКИ и СЕРИИ ПОБЕД (берём из player.json)
            # •	угадал с 1 попытки: x2 рыбок
            # •	серия побед (3+ подряд): +1 рыбка к каждой следующей победе в серии
            # открытие чтение запись фала
            # РИСУЕМ ТЕКСТ self.width / 2, self.height / 2
            # ЗАГРУЖАЕМ В ПРОГРЕСС

        elif self.game_res == "loss":
            arcade.draw_texture_rect(self.single_loss_tex,
                                     arcade.rect.XYWH(self.width / 2,
                                                      self.height / 2,
                                                      self.single_win_tex.width * scale,
                                                      self.height))

        elif self.game_res == "draw" or "left_win" or "right_win" or "all_loss":
            arcade.draw_texture_rect(self.single_win_tex,
                                     arcade.rect.XYWH(self.width / 2,
                                                      self.height / 2,
                                                      self.single_win_tex.width * scale,
                                                      self.height))
        # -- из progress_screen.py --
        # повыше по y и побольше в масштабе
        #
        # exit_height = btn_height * 0.8
        # exit_width = self.exit_btn_tex.width * (exit_height / self.exit_btn_tex.height)
        #
        # self.exit_rect = arcade.rect.XYWH(self.width / 2,
        #                                   exit_height,
        #                                   exit_width,
        #                                   exit_height)
        #
        # arcade.draw_texture_rect(self.home_btn_tex, self.exit_rect)
        #
        # if self.exit_hover:
        #     arcade.draw_lrbt_rectangle_outline(self.exit_rect.left,
        #                                        self.exit_rect.right,
        #                                        self.exit_rect.bottom,
        #                                        self.exit_rect.top,
        #                                        arcade.color.YELLOW,
        #                                        3)


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