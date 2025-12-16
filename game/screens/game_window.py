import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Meowdex"


class MainWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title, resizable=True)
        self.texture = arcade.load_texture("../images/background/blue_shtori.jpg")

    def setup(self):
        """ Инициализируем игру здесь. Вызывается один раз при запуске игры """
        pass

    def on_draw(self):
        """ Главная функция рисования содержимого окна. Вызывается каждый кадр """
        self.clear()
        arcade.draw_texture_rect(self.texture, arcade.rect.XYWH(SCREEN_WIDTH // 2,
                                                                SCREEN_HEIGHT // 2,
                                                                SCREEN_WIDTH,
                                                                SCREEN_HEIGHT))




def main():
    game = MainWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()