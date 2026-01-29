# игра с другом
import arcade


class FriendGameScreen(arcade.View):
    def __init__(self, left_word, right_word, difficulty):
        super().__init__()

        self.left_word = left_word
        self.right_word = right_word

        self.left_size = len(left_word)
        self.right_size = len(right_word)
