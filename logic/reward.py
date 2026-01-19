# логика начислений за результат раунда (рыбки, серия побед, повышение ранга)
from models.progress import Progress


def process_win(progress: Progress):
    progress.win_streak += 1
    # progress.fishes += ...


def process_loss(progress: Progress):
    progress.win_streak = 0