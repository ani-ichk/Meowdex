# сохранение и загрузка состояния игры во внешние файлы (прогресс игрока)
import json
from models.progress import Progress


def save_state(progress: Progress):
    data = {
        "rank": progress.rank,
        "fishes": progress.fishes,
        "win_streak": progress.win_streak
    }
    with open("data/player.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_state():
    with open("data/player.json", encoding="utf-8") as f:
        data = json.load(f)

    return Progress(
        rank=data["rank"],
        fishes=data["fishes"],
        win_streak=data["win_streak"]
    )