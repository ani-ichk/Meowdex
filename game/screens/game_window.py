import arcade
import random
import time

SCREEN_TITLE = "Meowdex"


class Player:
    def __init__(self, nickname):
        self.nickname = nickname
        self.level = 0
        self.fish_cnt = 0
        self.streak = 0


class Character:
    def __init__(self, name):
        self.name = name
        self.dialogues = '../characters/dialogues.json'

    def get_dialogue(self, situation):
        pass


class Word:
    def __init__(self, word, difficulty):
        self.word = word.upper()
        self.difficulty = difficulty
        self.length = len(word)


class GameRound:
    def __init__(self, hidden_words, max_attempts):
        self.hidden_words = hidden_words
        self.max_attempts = max_attempts
        self.current_attempt = 0
        self.attempts_history = []
        self.is_completed = False
        self.result = None


class GameManager:
    def __init__(self):
        self.current_player = None
        self.game_mode = None
        self.current_difficulty = None


class Keyboard:
    def __init__(self):
        self.keys = [
            ['Й', 'Ц', 'У', 'К', 'Е', 'Н', 'Г', 'Ш', 'Щ', 'З', 'Х', 'Ъ'],
            ['Ф', 'Ы', 'В', 'А', 'П', 'Р', 'О', 'Л', 'Д', 'Ж', 'Э'],
            ['ENTER', 'Я', 'Ч', 'С', 'М', 'И', 'Т', 'Ь', 'Б', 'Ю', 'BACKSPACE']
        ]


class WordGrid:
    def __init__(self, row, col, cell_size):
        self.row = row
        self.col = col
        self.cell_size = cell_size
        self.grid = [[None for _ in range(col)] for _ in range(row)]


class MainView(arcade.View):
    """Основное меню"""

    def __init__(self):
        super().__init__()

        # Загружаем текстуры
        self.background_texture = arcade.load_texture("../../images/background/blue_shtori.jpg")
        self.logo_texture = arcade.load_texture("../../images/logo/logo.png")
        self.play_btn_texture = arcade.load_texture("../../images/button/play_btn.png")
        self.rating_btn_texture = arcade.load_texture("../../images/button/rating_btn.png")
        self.settings_btn_texture = arcade.load_texture("../../images/button/settings_btn.png")
        self.exit_btn_texture = arcade.load_texture("../../images/button/exit_btn.png")

        self.buttons_hover = {
            "play": False,
            "rating": False,
            "settings": False,
            "exit": False
        }

        # Анимационные переменные
        self.animation_timer = 0.0
        self.animating = False
        self.animation_progress = 0.0
        self.animation_duration = 0.8
        self.button_positions = []
        self.button_targets = []

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.animating = False
        self.animation_progress = 0.0
        self.animation_timer = 0.0

    def on_draw(self):
        self.clear()

        # Рисуем задний фон
        if (self.window.width / self.window.height) > (self.background_texture.width / self.background_texture.height):
            draw_width = self.background_texture.width * (self.window.height / self.background_texture.height)
            draw_height = self.window.height
        else:
            draw_width = self.window.width
            draw_height = self.background_texture.height * (self.window.width / self.background_texture.width)

        # Затемнение фона при анимации
        if self.animating:
            darken_alpha = int(150 * self.animation_progress)
            arcade.draw_texture_rect(self.background_texture,
                                     arcade.rect.XYWH(self.window.width // 2,
                                                      self.window.height // 2,
                                                      draw_width,
                                                      draw_height))
            arcade.draw_rectangle_filled(self.window.width // 2,
                                         self.window.height // 2,
                                         self.window.width,
                                         self.window.height,
                                         (0, 0, 0, darken_alpha))
        else:
            arcade.draw_texture_rect(self.background_texture,
                                     arcade.rect.XYWH(self.window.width // 2,
                                                      self.window.height // 2,
                                                      draw_width,
                                                      draw_height))

        # Логотип
        logo_height = self.window.height / 3
        logo_width = self.logo_texture.width * (logo_height / self.logo_texture.height)
        logo_y = self.window.height - (logo_height // 2)

        logo_alpha = 255
        if self.animating:
            logo_alpha = int(255 * (1 - self.animation_progress))

        arcade.draw_texture_rect(self.logo_texture,
                                 arcade.rect.XYWH(self.window.width // 2,
                                                  logo_y,
                                                  logo_width,
                                                  logo_height),
                                 alpha=logo_alpha)

        btn_height = self.window.height / 10
        start_y = self.window.height // 1.8
        spacing = btn_height * 1.2

        # Список кнопок
        buttons = [
            (self.play_btn_texture, "play"),
            (self.rating_btn_texture, "rating"),
            (self.settings_btn_texture, "settings"),
            (self.exit_btn_texture, "exit")
        ]

        # Рисуем кнопки с учетом анимации
        for i, (texture, btn_type) in enumerate(buttons):
            btn_width = texture.width * (btn_height / texture.height)

            if self.animating:
                if i < len(self.button_positions):
                    start_pos = self.button_positions[i]
                    target_pos = self.button_targets[i]
                    current_y = start_pos + (target_pos - start_pos) * self.animation_progress
                    alpha = int(255 * (1 - self.animation_progress))
                    arcade.draw_texture_rect(texture,
                                             arcade.rect.XYWH(self.window.width // 2,
                                                              current_y,
                                                              btn_width,
                                                              btn_height),
                                             alpha=alpha)
            else:
                btn_y = start_y - (i * spacing)
                if self.buttons_hover[btn_type]:
                    arcade.draw_rectangle_filled(self.window.width // 2, btn_y,
                                                 btn_width * 1.1, btn_height * 1.1,
                                                 arcade.color.GOLDEN_BROWN + (100,))
                arcade.draw_texture_rect(texture,
                                         arcade.rect.XYWH(self.window.width // 2,
                                                          btn_y,
                                                          btn_width,
                                                          btn_height))

    def on_update(self, delta_time):
        if self.animating:
            self.animation_timer += delta_time
            self.animation_progress = self.animation_timer / self.animation_duration

            if self.animation_progress >= 1.0:
                level_view = LevelView()
                self.window.show_view(level_view)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.animating:
            return

        btn_height = self.window.height / 10
        start_y = self.window.height // 1.8
        spacing = btn_height * 1.2

        buttons = ["play", "rating", "settings", "exit"]
        for i, btn_type in enumerate(buttons):
            btn_y = start_y - (i * spacing)
            btn_width = self.play_btn_texture.width * (btn_height / self.play_btn_texture.height)

            if (self.window.width // 2 - btn_width // 2 < x < self.window.width // 2 + btn_width // 2 and
                    btn_y - btn_height // 2 < y < btn_y + btn_height // 2):
                self.buttons_hover[btn_type] = True
            else:
                self.buttons_hover[btn_type] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.animating:
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            btn_height = self.window.height / 10
            start_y = self.window.height // 1.8
            spacing = btn_height * 1.2

            buttons = ["play", "rating", "settings", "exit"]
            for i, btn_type in enumerate(buttons):
                btn_y = start_y - (i * spacing)
                btn_width = self.play_btn_texture.width * (btn_height / self.play_btn_texture.height)

                if (self.window.width // 2 - btn_width // 2 < x < self.window.width // 2 + btn_width // 2 and
                        btn_y - btn_height // 2 < y < btn_y + btn_height // 2):

                    if btn_type == "play":
                        self.animating = True
                        self.animation_timer = 0.0
                        self.animation_progress = 0.0

                        self.button_positions = []
                        self.button_targets = []
                        for j in range(len(buttons)):
                            btn_y_pos = start_y - (j * spacing)
                            self.button_positions.append(btn_y_pos)
                            if j % 2 == 0:
                                target_y = -100
                            else:
                                target_y = self.window.height + 100
                            self.button_targets.append(target_y)
                    elif btn_type == "exit":
                        self.window.close()
                    else:
                        print(f"Нажата кнопка: {btn_type}")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)


class LevelView(arcade.View):

    def __init__(self):
        super().__init__()

        # Загружаем текстуры
        self.single_mod = arcade.load_texture("../../images/button/play_btn.png")
        self.friend_mod = arcade.load_texture("../../images/button/play_btn.png")
        self.light_lvl = arcade.load_texture("../../images/button/play_btn.png")
        self.middle_lvl = arcade.load_texture("../../images/button/play_btn.png")
        self.hard_lvl = arcade.load_texture("../../images/button/play_btn.png")
        self.expert_lvl = arcade.load_texture("../../images/button/play_btn.png")
        self.word_from_base = arcade.load_texture("../../images/button/play_btn.png")
        self.user_input = arcade.load_texture("../../images/button/play_btn.png")

        self.background_texture_left = arcade.load_texture("../../images/background/blue_shtori_left.jpg")
        self.background_texture_right = arcade.load_texture("../../images/background/blue_shtori_right.jpg")

        self.back_btn = arcade.load_texture("../../images/button/exit_btn.png")

        self.buttons_hover = {
            "light": False,
            "middle": False,
            "hard": False,
            "expert": False
        }

        # Анимационные переменные
        self.buttons_appear_start = 0.0
        self.buttons_appear_progress = 0.0
        self.buttons_appear_duration = 0.5

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.buttons_appear_start = time.time()
        self.buttons_appear_progress = 0.0

    def on_draw(self):
        self.clear()
        # 1. Рисуем фон - две склеенные фотографии
        self._draw_background()

        # 2. Рисуем интерфейс поверх фона
        self._draw_interface()

        # 3. Кнопка "Назад" - поверх всего
        self._draw_back_button()

    def _draw_background(self):
        """Рисует две фотографии фона, которые склеиваются посередине"""
        # Половина ширины экрана
        half_width = self.window.width // 2

        # Рассчитываем размеры для сохранения пропорций

        # Левая фотография
        # Масштабируем по высоте окна, сохраняя пропорции
        left_scale = self.window.height / self.background_texture_left.height
        left_width = self.background_texture_left.width * left_scale
        left_height = self.window.height

        # Правая фотография
        # Масштабируем по высоте окна, сохраняя пропорции
        right_scale = self.window.height / self.background_texture_right.height
        right_width = self.background_texture_right.width * right_scale
        right_height = self.window.height

        # Позиционируем фотографии так, чтобы они склеивались посередине

        # Левая фотография: правый край на середине экрана
        left_x = half_width - left_width // 2
        left_center_x = left_x + left_width // 2

        # Правая фотография: левый край на середине экрана
        right_x = half_width - right_width // 2
        right_center_x = right_x + right_width // 2

        # Рисуем левую фотографию
        arcade.draw_texture_rect(self.background_texture_left,
                                 arcade.rect.XYWH(left_center_x,
                                                  self.window.height // 2,
                                                  left_width,
                                                  left_height))

        # Рисуем правую фотографию
        arcade.draw_texture_rect(self.background_texture_right,
                                 arcade.rect.XYWH(right_center_x,
                                                  self.window.height // 2,
                                                  right_width,
                                                  right_height))

    def _draw_interface(self):
        """Рисует интерфейс с кнопками поверх фона"""
        scale = self.buttons_appear_progress
        if scale <= 0:
            return

        # Половина ширины экрана
        half_width = self.window.width // 2

        # Рисуем левую половину (Одиночный режим)
        self._draw_left_half_interface(half_width, scale)

        # Рисуем правую половину (Режим с другом)
        self._draw_right_half_interface(half_width, scale)

    def _draw_left_half_interface(self, half_width, scale):
        """Рисует интерфейс в левой половине экрана"""
        # Заголовок "Одиночный режим" - вверху левой половины
        header_height = self.window.height * 0.85
        header_width = self.single_mod.width * (header_height / self.single_mod.height * 0.3)

        header_center_x = half_width // 2  # Центр левой половины
        header_center_y = self.window.height * 0.8

        if scale > 0:
            arcade.draw_texture_rect(self.single_mod,
                                     arcade.rect.XYWH(header_center_x,
                                                      header_center_y,
                                                      header_width * scale,
                                                      header_height * 0.3 * scale),
                                     alpha=int(255 * scale))

        # 4 кнопки уровней сложности под заголовком
        level_buttons = [
            (self.light_lvl, "light", self.window.height * 0.6),
            (self.middle_lvl, "middle", self.window.height * 0.45),
            (self.hard_lvl, "hard", self.window.height * 0.3),
            (self.expert_lvl, "expert", self.window.height * 0.15)
        ]

        for texture, btn_type, y_pos in level_buttons:
            btn_height = self.window.height * 0.1
            btn_width = texture.width * (btn_height / texture.height)
            btn_center_x = half_width // 2

            # Подсветка при наведении
            if scale >= 1.0 and self.buttons_hover[btn_type]:
                arcade.draw_rectangle_filled(btn_center_x, y_pos,
                                             btn_width * 1.1, btn_height * 1.1,
                                             arcade.color.GOLDEN_BROWN + (100,))

            # Рисуем кнопку
            if scale > 0:
                arcade.draw_texture_rect(texture,
                                         arcade.rect.XYWH(btn_center_x,
                                                          y_pos,
                                                          btn_width * scale,
                                                          btn_height * scale),
                                         alpha=int(255 * scale))

    def _draw_right_half_interface(self, half_width, scale):
        """Рисует интерфейс в правой половине экрана"""
        # Заголовок "Режим с другом" - вверху правой половины
        header_height = self.window.height * 0.85
        header_width = self.friend_mod.width * (header_height / self.friend_mod.height * 0.3)

        header_center_x = half_width + half_width // 2  # Центр правой половины
        header_center_y = self.window.height * 0.8

        if scale > 0:
            arcade.draw_texture_rect(self.friend_mod,
                                     arcade.rect.XYWH(header_center_x,
                                                      header_center_y,
                                                      header_width * scale,
                                                      header_height * 0.3 * scale),
                                     alpha=int(255 * scale))

        # 2 кнопки под заголовком
        friend_buttons = [
            (self.word_from_base, "word_base", self.window.height * 0.45),
            (self.user_input, "user_word", self.window.height * 0.3)
        ]

        for texture, btn_type, y_pos in friend_buttons:
            btn_height = self.window.height * 0.1
            btn_width = texture.width * (btn_height / texture.height)
            btn_center_x = half_width + half_width // 2

            # Рисуем кнопку
            if scale > 0:
                arcade.draw_texture_rect(texture,
                                         arcade.rect.XYWH(btn_center_x,
                                                          y_pos,
                                                          btn_width * scale,
                                                          btn_height * scale),
                                         alpha=int(255 * scale))

    def _draw_back_button(self):
        """Рисует кнопку 'Назад' внизу по центру"""
        scale = self.buttons_appear_progress
        if scale <= 0:
            return

        back_btn_height = self.window.height / 15
        back_btn_y = back_btn_height * 1.2
        back_btn_width = self.back_btn.width * (back_btn_height / self.back_btn.height)

        # # Подсветка при наведении
        # if scale >= 1.0 and self.buttons_hover["back"]:
        #     arcade.draw_rectangle_filled(self.window.width // 2,
        #                                  back_btn_y,
        #                                  back_btn_width * 1.1,
        #                                  back_btn_height * 1.1,
        #                                  arcade.color.GRAY + (100,))

        # Рисуем кнопку
        if scale > 0:
            arcade.draw_texture_rect(self.back_btn,
                                     arcade.rect.XYWH(self.window.width // 2,
                                                      back_btn_y,
                                                      back_btn_width * scale,
                                                      back_btn_height * scale),
                                     alpha=int(255 * scale))

    def on_update(self, delta_time):
        """Обновление анимации появления кнопок"""
        elapsed_time = time.time() - self.buttons_appear_start
        self.buttons_appear_progress = min(1.0, elapsed_time / self.buttons_appear_duration)

    def on_mouse_motion(self, x, y, dx, dy):
        if self.buttons_appear_progress < 1.0:
            return

        half_width = self.window.width // 2

        # Проверяем кнопки левой половины (уровни сложности)
        level_buttons = [
            ("light", self.window.height * 0.6),
            ("middle", self.window.height * 0.45),
            ("hard", self.window.height * 0.3),
            ("expert", self.window.height * 0.15)
        ]

        for btn_type, y_pos in level_buttons:
            btn_height = self.window.height * 0.1
            btn_width = self.light_lvl.width * (btn_height / self.light_lvl.height)
            btn_center_x = half_width // 2

            if (btn_center_x - btn_width // 2 < x < btn_center_x + btn_width // 2 and
                    y_pos - btn_height // 2 < y < y_pos + btn_height // 2):
                self.buttons_hover[btn_type] = True
            else:
                self.buttons_hover[btn_type] = False

        # Проверяем кнопки правой половины
        friend_buttons = [
            ("word_base", self.window.height * 0.45),
            ("user_word", self.window.height * 0.3)
        ]

        for btn_type, y_pos in friend_buttons:
            btn_height = self.window.height * 0.1
            btn_width = self.word_from_base.width * (btn_height / self.word_from_base.height)
            btn_center_x = half_width + half_width // 2

            if (btn_center_x - btn_width // 2 < x < btn_center_x + btn_width // 2 and
                    y_pos - btn_height // 2 < y < y_pos + btn_height // 2):
                self.buttons_hover[btn_type] = True
            else:
                self.buttons_hover[btn_type] = False

        # Проверяем кнопку "Назад"
        back_btn_height = self.window.height / 15
        back_btn_y = back_btn_height * 1.2
        back_btn_width = self.back_btn.width * (back_btn_height / self.back_btn.height)

        if (self.window.width // 2 - back_btn_width // 2 < x < self.window.width // 2 + back_btn_width // 2 and
                back_btn_y - back_btn_height // 2 < y < back_btn_y + back_btn_height // 2):
            self.buttons_hover["back"] = True
        else:
            self.buttons_hover["back"] = False

    def on_mouse_press(self, x, y, button, modifiers):
        if self.buttons_appear_progress < 1.0:
            return

        if button == arcade.MOUSE_BUTTON_LEFT:
            half_width = self.window.width // 2

            # Проверка нажатия на кнопки уровней сложности
            level_buttons = [
                ("light", self.window.height * 0.6),
                ("middle", self.window.height * 0.45),
                ("hard", self.window.height * 0.3),
                ("expert", self.window.height * 0.15)
            ]

            for btn_type, y_pos in level_buttons:
                btn_height = self.window.height * 0.1
                btn_width = self.light_lvl.width * (btn_height / self.light_lvl.height)
                btn_center_x = half_width // 2

                if (btn_center_x - btn_width // 2 < x < btn_center_x + btn_width // 2 and
                        y_pos - btn_height // 2 < y < y_pos + btn_height // 2):
                    print(f"Выбран уровень сложности: {btn_type}")
                    # Здесь будет переход к игре на выбранном уровне

            # Проверка нажатия на кнопки правой половины
            friend_buttons = [
                ("word_base", self.window.height * 0.45),
                ("user_word", self.window.height * 0.3)
            ]

            for btn_type, y_pos in friend_buttons:
                btn_height = self.window.height * 0.1
                btn_width = self.word_from_base.width * (btn_height / self.word_from_base.height)
                btn_center_x = half_width + half_width // 2

                if (btn_center_x - btn_width // 2 < x < btn_center_x + btn_width // 2 and
                        y_pos - btn_height // 2 < y < y_pos + btn_height // 2):
                    print(f"Выбран режим: {btn_type}")
                    # Здесь будет переход к соответствующему режиму

            # Проверка нажатия на кнопку "Назад"
            back_btn_height = self.window.height / 15
            back_btn_y = back_btn_height * 1.2
            back_btn_width = self.back_btn.width * (back_btn_height / self.back_btn.height)

            if (self.window.width // 2 - back_btn_width // 2 < x < self.window.width // 2 + back_btn_width // 2 and
                    back_btn_y - back_btn_height // 2 < y < back_btn_y + back_btn_height // 2):
                main_view = MainView()
                self.window.show_view(main_view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)
        elif key == arcade.key.ESCAPE:
            main_view = MainView()
            self.window.show_view(main_view)


class MainWindow(arcade.Window):
    """Главное окно приложения"""

    def __init__(self, title):
        super().__init__(800, 600, title)

    def setup(self):
        main_view = MainView()
        self.show_view(main_view)


def main():
    game = MainWindow(SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()