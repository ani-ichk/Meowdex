class Progress:
    def __init__(self):
        self.total_fish = 0
        self.win_streak = 0

        self.rank_requirements = {
            1: 0,
            2: 10,
            3: 25,
            4: 50,
            5: 90,
            6: 150,
            7: 230,
            8: 330,
            9: 450,
            10: 600,
        }

        self.rank_names = {
            1: "Котёнок-зритель",
            2: "Любитель викторин",
            3: "Знаток слов",
            4: "Мастер угадайки",
            5: "Гуру «Мяудекса»",
            6: "Легенда шоу",
            7: "Чемпион эфира",
            8: "Король викторины",
            9: "Император слов",
            10: "БОГ «Мяудекса»",
        }


    def add_fish(self, amount: int):
        self.total_fish += amount


    def current_rank(self) -> int:
        for rank in sorted(self.rank_requirements.keys(), reverse=True):
            if self.total_fish >= self.rank_requirements[rank]:
                return rank
        return 1

    def current_rank_name(self) -> str:
        return self.rank_names[self.current_rank()]


    def next_rank(self):
        rank = self.current_rank()
        if rank >= 10:
            return None
        return rank + 1

    def next_rank_name(self):
        next_rank = self.next_rank()
        if next_rank is None:
            return "Максимальный ранг"
        return self.rank_names[next_rank]

    def next_rank_requirement(self):
        next_rank = self.next_rank()
        if next_rank is None:
            return self.rank_requirements[self.current_rank()]
        return self.rank_requirements[next_rank]

    def fish_progress_in_rank(self):
        rank = self.current_rank()
        return self.total_fish - self.rank_requirements[rank]
