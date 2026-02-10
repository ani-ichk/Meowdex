import arcade
import json
from pathlib import Path
import random


PLAYER_PATH = Path("data/player.json")

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

        self.single_win_tex = arcade.load_texture("data/images/label/win_result.png")
        self.single_loss_tex = arcade.load_texture("data/images/label/loss_result.png")
        self.friend_win_tex = arcade.load_texture("data/images/label/win_result.png")
        self.friend_loss_tex = arcade.load_texture("data/images/label/loss_result.png")
        self.draw_tex = arcade.load_texture("data/images/label/draw_result.png")
        self.fish_icon_tex = arcade.load_texture("data/images/label/fish_game.png")

        self.home_btn_tex = arcade.load_texture("data/images/button/home_btn.png")

        self.background_tex_left = arcade.load_texture("data/images/background/blue_shtori_left.jpg")
        self.background_tex_right = arcade.load_texture("data/images/background/blue_shtori_right.jpg")

        self.win_particles = []
        self.win_particles_active = False

        # Проигрыш
        self.rain = []
        self.rain_active = False

        self.difficulty = difficulty
        self.attempt = attempt
        self.game_res = game_res

        self.home_rect = None
        self.home_hover = False

        self.screen_state = "closed"
        self.left_position = 0.0
        self.right_position = 0.0
        self.animation_speed = 2.0

        self.fade_mode = None
        self.fade_alpha = 0
        self.fade_active = False
        self.fade_speed = 600

        # progress
        self.fish_gained = 0
        self.fishes = 0
        self.win_streak = 0

    def on_show_view(self):
        self.fade_alpha = 255
        self.fade_active = True
        self.fade_mode = "on"

        self.screen_state = "opening"
        if self.game_res == "win":
            self.spawn_win_particles()
        elif self.game_res == "loss":
            self.spawn_rain()

        self.apply_result()

    def load_player(self):
        if not PLAYER_PATH.exists():
            return {
                "fishes": 0,
                "win_streak": 0
            }

        with open(PLAYER_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_player(self, data):
        with open(PLAYER_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def calculate_fish(self, win_streak: int):
        BASE_FISH = {
            "easy": 2,
            "normal": 4,
            "hard": 6,
            "expert": 8
        }

        # 1. базовая награда по сложности
        fish = BASE_FISH.get(self.difficulty, 0)

        # 2. первая попытка → x2
        if self.attempt == 1:
            fish *= 2

        return fish

    def apply_result(self):
        player = self.load_player()

        if self.game_res == "win":
            fish = self.calculate_fish(player["win_streak"])
            self.fish_gained = fish

            player["fishes"] += fish
            player["win_streak"] += 1

        elif self.game_res == "loss":
            self.fish_gained = 0
            player["win_streak"] = 0

        else:  # draw / friend / etc
            self.fish_gained = 0

        self.fishes = player.get("fishes", 0)

        self.win_streak = player["win_streak"]

        self.save_player(player)

    def spawn_win_particles(self):
        self.win_particles.clear()

        for _ in range(120):
            x = random.uniform(0, self.width)
            y = self.height + random.uniform(0, 200)

            vx = random.uniform(-40, 40)
            vy = random.uniform(-120, -260)

            radius = random.uniform(4, 7)

            color = random.choice([
                arcade.color.YELLOW,
                arcade.color.ORANGE,
                arcade.color.LIME_GREEN,
                arcade.color.SKY_BLUE,
                arcade.color.PINK
            ])

            self.win_particles.append(
                [x, y, vx, vy, radius, color]
            )

        self.win_particles_active = True

    def spawn_rain(self):
        self.rain.clear()

        for _ in range(160):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)

            speed = random.uniform(300, 600)
            length = random.uniform(10, 20)

            self.rain.append([x, y, speed, length])

        self.rain_active = True

    def on_draw(self):
        self.clear()

        # Блюр добавить после заднего фона ##############
        arcade.draw_lrbt_rectangle_filled(
                0, self.width, 0, self.height,
                (0, 0, 0, 150)
            )
        #################################
        # отрисовка частиц
        if self.win_particles_active:
            for x, y, vx, vy, radius, color in self.win_particles:
                arcade.draw_circle_filled(
                    x,
                    y,
                    radius,
                    color
                )

        if self.rain_active:
            for x, y, speed, length in self.rain:
                arcade.draw_line(
                    x,
                    y,
                    x,
                    y + length,
                    arcade.color.SLATE_GRAY,
                    2
                )

        scale = self.height / self.single_win_tex.height

        if self.game_res == "win":
            arcade.draw_texture_rect(self.single_win_tex,
                                     arcade.rect.XYWH(self.width / 2,
                                                      self.height / 2,
                                                      self.single_win_tex.width * scale,
                                                      self.height))
        if self.game_res == "win":
            y_pos = self.height * 0.40

            # Текст "+X"
            arcade.draw_text(
                f"+{self.fish_gained}",
                self.width / 2 - 30,
                y_pos,
                arcade.color.GOLD,
                font_size=42,
                anchor_x="right",
                anchor_y="center",
                bold=True
            )

            # Иконка рыбки
            icon_size = 100
            arcade.draw_texture_rect(
                self.fish_icon_tex,
                arcade.rect.XYWH(
                    self.width / 2 + 10,
                    y_pos,
                    icon_size,
                    icon_size
                )
            )


        elif self.game_res == "loss":
            arcade.draw_texture_rect(self.single_loss_tex,
                                    arcade.rect.XYWH(self.width / 2,
                                                    self.height / 2,
                                                    self.single_win_tex.width * scale,
                                                    self.height))
        elif self.game_res in ("draw", "left_win", "right_win", "all_loss"):
            arcade.draw_texture_rect(self.draw_tex,
                                     arcade.rect.XYWH(self.width / 2,
                                                      self.height / 2,
                                                      self.single_win_tex.width * scale,
                                                      self.height))
        else:
            arcade.draw_texture_rect(self.single_loss_tex,
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
            # ЗАГРУЖАЕМ В ПРОГРЕСС (Meowdex/logic/progres.py)

        # elif self.game_res == "loss":
        #     arcade.draw_texture_rect(self.single_loss_tex,
        #                              arcade.rect.XYWH(self.width / 2,
        #                                               self.height / 2,
        #                                               self.single_win_tex.width * scale,
        #                                               self.height))
        #
        # elif self.game_res == "draw" or "left_win" or "right_win" or "all_loss":
        #     arcade.draw_texture_rect(self.single_win_tex,
        #                              arcade.rect.XYWH(self.width / 2,
        #                                               self.height / 2,
        #                                               self.single_win_tex.width * scale,
        #                                               self.height))
        # -- из progress_screen.py --
        # повыше по y и побольше в масштабе
        #
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

                    from ui.screens.menu_screen import MenuScreen
                    self.window.show_view(MenuScreen())
        if self.win_particles_active:
            for p in self.win_particles:
                p[0] += p[2] * delta_time  # x
                p[1] += p[3] * delta_time  # y

            self.win_particles = [
                p for p in self.win_particles
                if p[1] > -50
            ]

        if self.rain_active:
            for drop in self.rain:
                drop[1] -= drop[2] * delta_time

                if drop[1] < -drop[3]:
                    drop[0] = random.uniform(0, self.width)
                    drop[1] = self.height + random.uniform(0, 200)

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