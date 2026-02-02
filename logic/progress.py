import json
import os


class Progress:
    FILE = "player.json"

    def __init__(self, fish=0):
        self.fish = fish
        self.win_streak = 0

    @classmethod
    def load(cls):
        if not os.path.exists(cls.FILE):
            return cls()
        with open(cls.FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(fish=data.get("fish", 0))

    def save(self):
        with open(self.FILE, "w", encoding="utf-8") as f:
            json.dump({"fish": self.fish}, f, ensure_ascii=False, indent=2)

    def current_rank(self):
        current_rank = 0
        if 0 < self.fish < 10:
            current_rank = 1
        elif 10 < self.fish < 25:
            current_rank = 2
        elif 25 < self.fish < 50:
            current_rank = 3
        elif 50 < self.fish < 90:
            current_rank = 4
        elif 90 < self.fish < 150:
            current_rank = 5
        elif 150 < self.fish < 230:
            current_rank = 6
        elif 230 < self.fish < 330:
            current_rank = 7
        elif 330 < self.fish < 450:
            current_rank = 8
        elif 450 < self.fish < 600:
            current_rank = 9
        elif self.fish > 600:
            current_rank = 10
        return current_rank

    def next_rank(self):
        current_rank = self.current_rank()
        next_rank = 0
        if current_rank == 1:
            next_rank = 2
        elif current_rank == 2:
            next_rank = 3
        elif current_rank == 3:
            next_rank = 4
        elif current_rank == 4:
            next_rank = 5
        elif current_rank == 5:
            next_rank = 6
        elif current_rank == 6:
            next_rank = 7
        elif current_rank == 7:
            next_rank = 8
        elif current_rank == 8:
            next_rank = 9
        elif current_rank == 9:
            next_rank = 10
        return next_rank

    def add_win(self):
        self.win_streak += 1

    def reset_streak(self):
        self.win_streak = 0
