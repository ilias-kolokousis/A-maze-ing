import configparser
import random

# 42 is 7x5!
# def set_entry(width: int, height: int):


def plot_42(left: int, top: int):
    x = 1
    y = 0
    coords = []
    while x < 8:
        if x == 1 or 5 <= x <= 7:
            coords += [f"{x + left},{top - y}"]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if x == 1 or x == 7:
            coords += [f"{x + left},{top - y}"]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if 1 <= x <= 3 or 5 <= x <= 7:
            coords += [f"{x + left},{top - y}"]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if x == 3 or x == 5:
            coords += [f"{x + left},{top - y}"]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if x == 3 or 5 <= x <= 7:
            coords += [f"{x + left},{top - y}"]
        x += 1
    return coords


def set_42_coordinates(width: int, height: int):
    if width < 9 or height < 7:
        return None

    pad_right = int((width - 7) / 2)
    if (width % 2) == 0:
        pad_left = pad_right + 1
    else:
        pad_left = pad_right
    print(f"Pad_right: {pad_right}")
    print(f"Pad_left: {pad_left}")

    pad_top = int((height - 5) / 2)
    if (height % 2) == 0:
        pad_bottom = pad_top + 1
    else:
        pad_bottom = pad_top
    print(f"Pad_top: {pad_top}")
    print(f"Pad_bottom: {pad_bottom}")

    coord_list = plot_42(pad_left, height - pad_top)
    coord_str = ""
    for x in range(len(coord_list)):
        if x != len(coord_list) - 1:
            coord_str += f"{coord_list[x]}:"
        else:
            coord_str += coord_list[x]
    print(coord_str)
    return coord_str


def generate_seed_config(seed: int):
    config = configparser.ConfigParser()
    random.seed(seed)
    width = random.randrange(4, 40)
    height = random.randrange(4, width)
    coord_42 = set_42_coordinates(width, height)
    entry = str(f"{random.randrange(1, width)},{random.randrange(1, height)}")
    exit = str(f"{random.randrange(1, width)},{random.randrange(1, height)}")
    perfect = random.choice([True, False])
    output = "maze.txt"

    config['custom'] = {
        "SEED": seed,
        "WIDTH": width,
        "HEIGHT": height,
        "ENTRY": entry,
        "EXIT": exit,
        "OUTPUT_FILE": output,
        "PERFECT": perfect,
        "42_COORDS": coord_42}

    with open('./src/custom_config.ini', 'w') as configfile:
        config.write(configfile)


def generate_random_config():
    x = input('Use default settings? (y/n)      ')
    if (x == 'y' or x == 'yes' or x == 'YES'):
        return True
    elif (x == 'n' or x == 'no' or x == 'NO'):
        is_seed = input('Use a seed? (y/n)      ')
        if (is_seed == 'y' or is_seed == 'yes' or is_seed == 'YES'):
            valid_seed = False
            for x in range(3):
                try:
                    seed = int(input('Seed:'))
                    valid_seed = True
                    break
                except ValueError as e:
                    print(f"Seed needs to be an integer: {e}")
                    print(f"Try {x + 1}/3")
                    if x == 2:
                        print("Continueing with random seed...")
            if valid_seed:
                generate_seed_config(seed)
            else:
                seed = random.randint(0, 999999999999999999)
                generate_seed_config(seed)
                print(f"Seed: {seed}")
        elif (
            is_seed == 'n' or
            is_seed == 'no' or is_seed == 'NO'
        ):
            seed = random.randint(0, 999999999999999999)
            generate_seed_config(seed)
            print(f"Seed: {seed}")
    else:
        go_again = input(
            'Could not understand your input, do you want to retry? (y/n)'
        )
        if (go_again == 'y' or go_again == 'yes' or go_again == 'YES'):
            generate_random_config()
        else:
            exit()
