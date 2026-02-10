import arcade
from ui.screens.result_screen import ResultScreen
from models.word import Word



# длина слова -> (кол-во букв, кол-во попыток)
GRID_CONFIG = {
    3: (3, 4),
    4: (4, 4),
    5: (5, 5),
    6: (6, 5),
    7: (7, 4),
    8: (8, 4),
    9: (9, 3),
}


class GameScreen(arcade.View):
    def __init__(self, target_word: str, difficulty: str):
        super().__init__()

        # -------- TEXTURES --------
        self.background_tex = arcade.load_texture("data/images/background/background.png")

        self.grid_textures = {
            3: arcade.load_texture("data/images/grids/grid_3.png"),
            4: arcade.load_texture("data/images/grids/grid_4.png"),
            5: arcade.load_texture("data/images/grids/grid_5.png"),
            6: arcade.load_texture("data/images/grids/grid_6.png"),
            7: arcade.load_texture("data/images/grids/grid_7.png"),
            8: arcade.load_texture("data/images/grids/grid_8.png"),
            9: arcade.load_texture("data/images/grids/grid_9.png"),
        }

        self.home_btn_tex = arcade.load_texture("data/images/button/home_btn.png")

        # -------- GAME DATA --------
        self.target_word = target_word.upper()
        self.word_obj = Word(self.target_word)
        self.difficulty = difficulty
        print(self.target_word)
        self.word_len = len(self.target_word)

        cols, rows = GRID_CONFIG.get(self.word_len, GRID_CONFIG[9])
        self.grid_cols = cols
        self.grid_rows = rows

        self.current_row = 0
        self.current_col = 0

        # grid[row][col] = {"letter": "", "state": None}
        self.grid = [
            [{"letter": "", "state": None} for _ in range(self.grid_cols)]
            for _ in range(self.grid_rows)
        ]

        self.game_res = None
        self.next_action = None

        # -------- UI --------
        self.home_rect = None
        self.home_hover = False

        # -------- TRANSITIONS --------
        self.fade_alpha = 0
        self.fade_active = False
        self.fade_mode = None
        self.fade_speed = 600

    # ---------------------------------------------------------------------

    def on_show_view(self):
        self.fade_alpha = 255
        self.fade_active = True
        self.fade_mode = "on"

    # ---------------------------------------------------------------------

    def on_draw(self):
        self.clear()

        # ----- BACKGROUND -----
        scale = self.height / self.background_tex.height
        arcade.draw_texture_rect(
            self.background_tex,
            arcade.rect.XYWH(
                self.width / 2,
                self.height / 2,
                self.background_tex.width * scale,
                self.height
            )
        )

        # ----- GRID -----
        grid_tex = self.grid_textures.get(self.grid_cols, self.grid_textures[9])
        grid_scale = 0.9

        grid_width = grid_tex.width * grid_scale
        grid_height = grid_tex.height * grid_scale

        grid_center_x = self.width / 2
        grid_center_y = self.height / 2 + 100

        arcade.draw_texture_rect(
            grid_tex,
            arcade.rect.XYWH(
                grid_center_x,
                grid_center_y,
                grid_width,
                grid_height
            )
        )

        # ----- LETTERS -----
        cell_w = grid_width / self.grid_cols
        cell_h = grid_height / self.grid_rows

        start_x = grid_center_x - grid_width / 2
        start_y = grid_center_y + grid_height / 2

        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                cell = self.grid[row][col]

                # координаты клетки
                x = start_x + col * cell_w + cell_w / 2
                y = start_y - row * cell_h - cell_h / 2

                # пустая клетка
                if not cell["letter"]:
                    continue

                # если буква уже проверена — рисуем PNG
                if cell["state"] is not None:
                    tex = self.get_letter_texture(cell["letter"], cell["state"])
                    if tex:
                        arcade.draw_texture_rect(
                            tex,
                            arcade.rect.XYWH(x, y, cell_h, cell_w)
                        )

                # если буква вводится прямо сейчас — рисуем текстом
                else:
                    arcade.draw_text(
                        cell["letter"],
                        x,
                        y,
                        arcade.color.WHITE,
                        font_size=48,
                        anchor_x="center",
                        anchor_y="center",
                        bold=True
                    )

        # ----- HOME BUTTON -----
        self.home_rect = arcade.rect.XYWH(
            self.width / 2,
            self.home_btn_tex.height * 2,
            self.home_btn_tex.width,
            self.home_btn_tex.height
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

        # ----- FADE -----
        if self.fade_active:
            arcade.draw_lrbt_rectangle_filled(
                0, self.width, 0, self.height,
                (0, 0, 0, int(self.fade_alpha))
            )

    # ---------------------------------------------------------------------

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

                elif self.next_action == "result":
                    self.window.show_view(
                        ResultScreen(
                            difficulty=self.difficulty,
                            attempt=self.current_row + 1,
                            game_res=self.game_res
                        )
                    )

    # ---------------------------------------------------------------------

    def on_mouse_motion(self, x, y, dx, dy):
        self.home_hover = False
        if self.home_rect:
            if self.home_rect.left <= x <= self.home_rect.right and \
               self.home_rect.bottom <= y <= self.home_rect.top:
                self.home_hover = True

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT and self.home_hover:
            self.next_action = "menu"
            self.fade_active = True
            self.fade_mode = "off"

    # ---------------------------------------------------------------------
    # INPUT
    # ---------------------------------------------------------------------
    def on_text(self, text):
        # принимаем ТОЛЬКО русские буквы
        if not text.isalpha():
            return

        letter = text.upper()

        # фильтр кириллицы
        if not ("А" <= letter <= "Я" or letter == "Ё"):
            return

        if self.current_col < self.grid_cols and self.current_row < self.grid_rows:
            self.grid[self.current_row][self.current_col]["letter"] = letter
            self.current_col += 1

    def on_key_press(self, key, modifiers):
        if key == arcade.key.BACKSPACE:
            if self.current_col > 0:
                self.current_col -= 1
                self.grid[self.current_row][self.current_col]["letter"] = ""

        elif key == arcade.key.ENTER:
            self.submit_row()

    # ---------------------------------------------------------------------
    # GAME LOGIC
    # ---------------------------------------------------------------------

    def submit_row(self):
        if self.current_col < self.grid_cols:
            return

        guess = "".join(cell["letter"] for cell in self.grid[self.current_row])
        print('self.grid:', self.grid)
        print('self.grid[self.current_row:', self.grid[self.current_row])
        print("guess:", guess)
        result = self.word_obj.check_guess(guess)

        for i, state in enumerate(result):
            self.grid[self.current_row][i]["state"] = state

        # WIN
        if guess == self.target_word:
            self.game_res = "win"
            self.next_action = "result"
            self.fade_active = True
            self.fade_mode = "off"
            return

        # NEXT ROW
        self.current_row += 1
        self.current_col = 0

        # LOSS
        if self.current_row >= self.grid_rows:
            self.game_res = "loss"
            self.next_action = "result"
            self.fade_active = True
            self.fade_mode = "off"

    # ---------------------------------------------------------------------
    # LETTER TEXTURES
    # ---------------------------------------------------------------------

    def get_letter_texture(self, letter, state):
        if not letter:
            return None

        if state == "correct":
            prefix = "З"
        elif state == "present":
            prefix = "О"
        elif state == "absent":
            prefix = "Ч"
        else:
            return None

        return arcade.load_texture(
            f"data/images/button/keyboard_btn/{prefix}_{letter}.png"
        )
