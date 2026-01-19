import arcade
from core.game_state import Game


def main():
    window = arcade.Window(
        width=1280,
        height=720,
        title="Meowdex"
    )
    game = Game(window)
    game.start()
    arcade.run()


if __name__ == '__main__':
    main()