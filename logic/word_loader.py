# загрузка слов из json по уровням сложности
import json
import random
from models.word import Word


def load_easy_word():
    with open("data/words/easy.json", encoding='utf-8') as f:
        words = json.load(f)

    return Word(random.choice(words))

def load_medium_word():
    with open("data/words/medium.json", encoding='utf-8') as f:
        words = json.load(f)

    return Word(random.choice(words))

def load_hard_word():
    with open("data/words/hard.json", encoding='utf-8') as f:
        words = json.load(f)

    return Word(random.choice(words))

def load_expert_word():
    with open("data/words/expert.json", encoding='utf-8') as f:
        words = json.load(f)

    return Word(random.choice(words))