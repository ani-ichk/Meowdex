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
    """Экран выбора уровня со шторками"""

    def __init__(self):
        super().__init__()

        # Текстуры шторок
        self.background_texture_left = arcade.load_texture("../../images/background/blue_shtori_left.jpg")
        self.background_texture_right = arcade.load_texture("../../images/background/blue_shtori_right.jpg")

        # Состояние шторок (True = открыта)
        self.left_opened = False
        self.right_opened = False

        # Текущая позиция анимации (0.0 = закрыта, 1.0 = открыта)
        self.left_position = 0.0
        self.right_position = 0.0

        # Скорость анимации
        self.animation_speed = 2.0

        # Для защиты от двойного клика
        self.last_click_time = 0

        # Анимационные переменные (таймер появления)
        self.buttons_appear_start = 0.0
        self.buttons_appear_progress = 0.0
        self.buttons_appear_duration = 0.5

    def on_show(self):
        """Вызывается при показе экрана"""
        arcade.set_background_color(arcade.color.BLACK)
        self.buttons_appear_start = time.time()
        # self.buttons_appear_progress = 0.0

        # Сбрасываем состояние
        self.left_opened = False
        self.right_opened = False
        self.left_position = 0.0
        self.right_position = 0.0
        self.last_click_time = 0

    def on_draw(self):
        """Отрисовка всего экрана"""
        self.clear()

        # Рисуем черный фон
        arcade.draw_rectangle_filled(self.window.width // 2,
                                     self.window.height // 2,
                                     self.window.width,
                                     self.window.height,
                                     arcade.color.BLACK)

        self._draw_curtains()

    def _draw_curtains(self):
        """Отрисовка двух шторок с анимацией"""
        center_x = self.window.width / 2
        center_y = self.window.height / 2

        # Рассчитываем размеры шторок
        left_scale = self.window.height / self.background_texture_left.height
        left_width = self.background_texture_left.width * left_scale
        left_height = self.window.height

        right_scale = self.window.height / self.background_texture_right.height
        right_width = self.background_texture_right.width * right_scale
        right_height = self.window.height

        # ===== ЛЕВАЯ ШТОРКА =====
        # При position=0: на месте (center_x - width/2)
        # При position=1: уехала влево (center_x - width/2 - width)
        left_offset = left_width * self.left_position
        left_center_x = center_x - left_width / 2 - left_offset

        # Рисуем левую шторку
        arcade.draw_texture_rect(
            self.background_texture_left,
            arcade.rect.XYWH(left_center_x, center_y, left_width, left_height)
        )

        # ===== ПРАВАЯ ШТОРКА =====
        # При position=0: на месте (center_x + width/2)
        # При position=1: уехала вправо (center_x + width/2 + width)
        right_offset = right_width * self.right_position
        right_center_x = center_x + right_width / 2 + right_offset

        # Рисуем правую шторку
        arcade.draw_texture_rect(
            self.background_texture_right,
            arcade.rect.XYWH(right_center_x, center_y, right_width, right_height)
        )

    def on_update(self, delta_time):
        """Обновление анимации каждый кадр"""
        # Обновляем анимацию появления кнопок
        elapsed_time = time.time() - self.buttons_appear_start
        self.buttons_appear_progress = min(1.0, elapsed_time / self.buttons_appear_duration)

        # Скорость анимации
        speed = self.animation_speed * delta_time

        # Анимация левой шторки
        target_left = 1.0 if self.left_opened else 0.0
        if abs(self.left_position - target_left) > 0.001:
            if self.left_position < target_left:
                self.left_position = min(target_left, self.left_position + speed)
            else:
                self.left_position = max(target_left, self.left_position - speed)

        # Анимация правой шторки
        target_right = 1.0 if self.right_opened else 0.0
        if abs(self.right_position - target_right) > 0.001:
            if self.right_position < target_right:
                self.right_position = min(target_right, self.right_position + speed)
            else:
                self.right_position = max(target_right, self.right_position - speed)

    def on_mouse_press(self, x, y, button, modifiers):
        """Обработка клика мыши"""
        if button != arcade.MOUSE_BUTTON_LEFT:
            return

        # Защита от двойного клика
        current_time = time.time()
        if current_time - self.last_click_time < 0.3:  # Защита от двойного клика
            return
        self.last_click_time = current_time

        if self.buttons_appear_progress < 1.0:
            return

        center_x = self.window.width / 2

        # Клик на левой половине - переключаем левую шторку. с правой точно так же
        if x < center_x:
            self.left_opened = not self.left_opened
        else:
            self.right_opened = not self.right_opened

    def on_key_press(self, key, modifiers):
        """Обработка нажатий клавиш"""
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