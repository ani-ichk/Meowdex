# ранг игрока:
# рыбки, тек. ранг, пороги уровней, проверку перехода на след. ранг
class Progress:
    def __init__(self, rank, fishes, win_streak):
        self.rank = rank
        self.fishes = fishes
        self.win_streak = win_streak

    def can_rank_up(self, required_fishes):
        return self.fishes >= required_fishes