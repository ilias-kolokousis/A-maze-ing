import random


def get_width(seed: str) -> str:
    i = 1
    width = ""
    while (seed[i] >= '0' and seed[i] <= '9'):
        width += seed[i]
        i += 1
    return width


def get_height(seed: str) -> str:
    i = 0
    height = ""
    while seed[i] != 'h':
        i += 1
    i += 1
    while (seed[i] >= '0' and seed[i] <= '9'):
        height += seed[i]
        i += 1
    return height


def get_entry_exit(width: str, height: str, seed: str) -> str:
    i = 0
    while seed[i] != 's':
        i += 1
    i += 1

    gen_seed = width + height
    while i < (len(seed) - 1):
        gen_seed += seed[i]
        i += 1

    gen_seed = int(gen_seed)
    w = int(width)
    h = int(height)
    random.seed(gen_seed)
    entry = f"{random.randint(1, w)},{random.randint(1, h)}"
    exit = f"{random.randint(1, w)},{random.randint(1, h)}"
    return entry, exit


def get_entry(width: str, height: str, seed: str) -> str:
    entry = get_entry_exit(width, height, seed)[0]
    return entry


def get_exit(width: str, height: str, seed: str) -> str:
    exit = get_entry_exit(width, height, seed)[1]
    return exit


def is_perfect(seed: str) -> str:
    i = len(seed) - 1
    if seed[i] == 't':
        return "True"
    else:
        return "False"


def is_valid_seed(seed: str) -> bool:
    i = 0
    if seed[i] != 'w':
        return False
    i += 1
    while seed[i] >= '0' and seed[i] <= '9':
        i += 1
    if seed[i] != 'h':
        return False
    i += 1
    while seed[i] >= '0' and seed[i] <= '9':
        i += 1
    if seed[i] != 's':
        return False
    i += 1
    while seed[i] >= '0' and seed[i] <= '9':
        i += 1
    if seed[i] != 't' and seed[i] != 'f':
        return False
    if len(seed) - 1 > i:
        return False
    return True
