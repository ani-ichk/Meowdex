# логика выбора реплик персонажей
import json
import random


def get_phrase(self, path, character, situation):
    with open(path, encoding='utf-8') as f:
        dialogs = json.load(f)
    return random.choice(dialogs[situation])