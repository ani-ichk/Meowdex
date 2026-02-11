import arcade
from logic.word import Word
from ui.screens.result_screen import ResultScreen

GRID_CONFIG = {
    3: (3, 4),
    4: (4, 4),
    5: (5, 5),
    6: (6, 5),
    7: (7, 4),
    8: (8, 4),
    9: (9, 3),
}


class ComputerGameScreen(arcade.View):
    def __init__(self, difficulty: str):
        super().__init__()
        self.difficulty = difficulty

        # Текстуры
        self.background_tex = arcade.load_texture("data/images/background/background.png")
        self.grid_textures = {n: arcade.load_texture(f"data/images/grids/grid_{n}.png") for n in range(3, 10)}
        self.home_btn_tex = arcade.load_texture("data/images/button/home_btn.png")

        # Компьютер выбирает слова для двух игроков
        word_left = Word.random_by_difficulty(difficulty)
        print(word_left)
        word_right = Word.random_by_difficulty(difficulty)
        print(word_right)
        # Игрок 0 угадывает слово игрока 2 (лево)
        # Игрок 1 угадывает слово игрока 1 (право)
        self.players = {
            0: self.create_player(word_left),
            1: self.create_player(word_right),
        }

        self.active_player = 0
        self.game_over = False
        self.winner = None
        self.loser = None
        self.result_type = None  # "left_win", "right_win", "draw", "all_loss"

        self.home_rect = None
        self.home_hover = False
        self.next_action = None

        self.fade_alpha = 0
        self.fade_active = False
        self.fade_mode = None
        self.fade_speed = 600

    def on_show_view(self):
        self.fade_alpha = 255
        self.fade_active = True
        self.fade_mode = "on"

    def create_player(self, target_word):
        target_word = target_word.upper()
        cols, rows = GRID_CONFIG[len(target_word)]
        return {
            "word": target_word,
            "word_obj": Word(target_word),
            "cols": cols,
            "rows": rows,
            "row": 0,
            "col": 0,
            "finished": False,  # Флаг завершения игрока (выиграл или закончились попытки)
            "won": False,  # Флаг победы игрока
            "attempts_used": 0,  # Использованные попытки
            "grid": [[{"letter": "", "state": None} for _ in range(cols)] for _ in range(rows)]
        }

    # ---------------------- Update / Fade ----------------------
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
                if self.next_action == "menu":
                    from ui.screens.menu_screen import MenuScreen
                    self.window.show_view(MenuScreen())

    # ---------------------- Drawing ----------------------
    def on_draw(self):
        self.clear()
        scale = self.height / self.background_tex.height
        arcade.draw_texture_rect(
            self.background_tex,
            arcade.rect.XYWH(self.width / 2, self.height / 2, self.background_tex.width * scale, self.height)
        )

        centers = [self.width / 4, self.width * 3 / 4]
        for idx in (0, 1):
            self.draw_player_grid(idx, centers[idx])

        if not self.game_over:
            arcade.draw_text(
                f"Ходит игрок {self.active_player + 1}",
                self.width / 2, self.height - 60,
                arcade.color.YELLOW, 26, anchor_x="center"
            )

        # HOME BUTTON
        self.home_rect = arcade.rect.XYWH(
            self.width / 2, self.home_btn_tex.height * 2,
            self.home_btn_tex.width, self.home_btn_tex.height
        )
        arcade.draw_texture_rect(self.home_btn_tex, self.home_rect)
        if self.home_hover:
            arcade.draw_lrbt_rectangle_outline(
                self.home_rect.left, self.home_rect.right,
                self.home_rect.bottom, self.home_rect.top,
                arcade.color.YELLOW, 3
            )

        # FADE
        if self.fade_active:
            arcade.draw_lrbt_rectangle_filled(
                0, self.width, 0, self.height,
                (0, 0, 0, int(self.fade_alpha))
            )

    # ---------------------- Grid Drawing ----------------------
    def draw_player_grid(self, idx, center_x):
        p = self.players[idx]
        grid_tex = self.grid_textures[p["cols"]]
        scale = 0.85
        gw, gh = grid_tex.width * scale, grid_tex.height * scale
        cy = self.height / 2 + 80

        arcade.draw_texture_rect(grid_tex, arcade.rect.XYWH(center_x, cy, gw, gh))
        cell_w, cell_h = gw / p["cols"], gh / p["rows"]
        sx, sy = center_x - gw / 2, cy + gh / 2

        for r in range(p["rows"]):
            for c in range(p["cols"]):
                cell = p["grid"][r][c]
                if not cell["letter"]:
                    continue
                x, y = sx + c * cell_w + cell_w / 2, sy - r * cell_h - cell_h / 2
                if cell["state"] is None:
                    arcade.draw_text(cell["letter"], x, y, arcade.color.WHITE, 32,
                                     anchor_x="center", anchor_y="center", bold=True)
                else:
                    tex = self.get_letter_texture(cell["letter"], cell["state"])
                    arcade.draw_texture_rect(tex, arcade.rect.XYWH(x, y, cell_h, cell_w))

    # ---------------------- Input ----------------------
    def on_text(self, text):
        if self.game_over or not text.isalpha():
            return
        letter = text.upper()
        if not ("А" <= letter <= "Я" or letter == "Ё"):
            return
        p = self.players[self.active_player]
        if p["col"] < p["cols"] and not p["finished"]:
            p["grid"][p["row"]][p["col"]]["letter"] = letter
            p["col"] += 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.window.set_fullscreen(not self.window.fullscreen)
        elif key == arcade.key.ESCAPE and self.window.fullscreen:
            self.window.set_fullscreen(False)

        if self.game_over:
            return

        p = self.players[self.active_player]
        if p["finished"]:
            # Если текущий игрок уже завершил, переключаем на другого
            self.switch_to_next_active_player()
            return

        if key == arcade.key.BACKSPACE and p["col"] > 0:
            p["col"] -= 1
            p["grid"][p["row"]][p["col"]]["letter"] = ""
        elif key == arcade.key.ENTER:
            self.submit_turn()

    def on_mouse_motion(self, x, y, dx, dy):
        self.home_hover = False
        if self.home_rect and self.home_rect.left <= x <= self.home_rect.right and \
                self.home_rect.bottom <= y <= self.home_rect.top:
            self.home_hover = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.home_hover:
            self.next_action = "menu"
            self.fade_active = True
            self.fade_mode = "off"

    # ---------------------- Game Logic ----------------------
    def submit_turn(self):
        p = self.players[self.active_player]
        if p["col"] < p["cols"]:
            return

        guess = "".join(cell["letter"] for cell in p["grid"][p["row"]])
        result = p["word_obj"].check_guess(guess)

        for i, state in enumerate(result):
            p["grid"][p["row"]][i]["state"] = state

        p["attempts_used"] = p["row"] + 1

        # если угадал
        if guess == p["word"]:
            p["won"] = True
            p["finished"] = True
            self.check_game_result()
            return

        # переход на следующую строку
        p["row"] += 1
        p["col"] = 0

        # если закончились попытки
        if p["row"] >= p["rows"]:
            p["finished"] = True
            self.check_game_result()
            return

        # смена активного игрока
        self.switch_to_next_active_player()

    def switch_to_next_active_player(self):
        """Переключает активного игрока на того, кто еще не завершил игру"""
        next_player = 1 - self.active_player

        # Если следующий игрок завершил, проверяем результат игры
        if self.players[next_player]["finished"]:
            # Оба игрока завершили
            self.check_game_result()
        else:
            # Переключаем на следующего игрока
            self.active_player = next_player

    def check_game_result(self):
        """Проверяет результат игры, когда оба игрока завершили"""
        p0 = self.players[0]
        p1 = self.players[1]

        # Проверяем, все ли игроки завершили
        if not (p0["finished"] and p1["finished"]):
            # Игра еще не окончена, переключаем на другого игрока
            if p0["finished"] and not p1["finished"]:
                self.active_player = 1
            elif p1["finished"] and not p0["finished"]:
                self.active_player = 0
            return

        # Все игроки завершили - определяем окончательный результат
        self.game_over = True

        if p0["won"] and p1["won"]:
            # Оба выиграли - ничья
            self.result_type = "draw"
        elif p0["won"]:
            # Игрок 0 (левый) выиграл
            self.result_type = "left_win"
            self.winner = 0
            self.loser = 1
        elif p1["won"]:
            # Игрок 1 (правый) выиграл
            self.result_type = "right_win"
            self.winner = 1
            self.loser = 0
        else:
            # Никто не выиграл - ничья (оба проиграли)
            self.result_type = "all_loss"

        # Определяем количество попыток для награды
        if self.result_type == "left_win":
            winner_attempt = p0["attempts_used"]
        elif self.result_type == "right_win":
            winner_attempt = p1["attempts_used"]
        else:
            winner_attempt = 0

        # Показываем экран результата
        self.window.show_view(
            ResultScreen(
                difficulty=self.difficulty,
                attempt=winner_attempt,
                game_res=self.result_type
            )
        )

    # ---------------------- Helper ----------------------
    def get_letter_texture(self, letter, state):
        prefix = {"correct": "З", "present": "О", "absent": "Ч"}.get(state)
        if not prefix:
            return None
        return arcade.load_texture(f"data/images/button/keyboard_btn/{prefix}_{letter}.png")