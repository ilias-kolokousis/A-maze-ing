import configparser
import random


def plot_42(left: int, top: int):
    x = 0
    y = 0
    coords = []
    while x < 8:
        if x == 1 or 5 <= x <= 7:
            coords += [(x + left, top + y)]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if x == 1 or x == 7:
            coords += [(x + left, top + y)]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if 1 <= x <= 3 or 5 <= x <= 7:
            coords += [(x + left, top + y)]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if x == 3 or x == 5:
            coords += [(x + left, top + y)]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if x == 3 or 5 <= x <= 7:
            coords += [(x + left, top + y)]
        x += 1
    return coords


def set_42_coordinates(width: int, height: int):
    if width < 9 or height < 7:
        return None

    pad_left = int((width - 8) / 2)

    pad_top = int((height - 5) / 2)

    coord_list = plot_42(pad_left, pad_top)
    coord_str = ""
    for x in range(len(coord_list)):
        if x != len(coord_list) - 1:
            coord_str += f"{coord_list[x][0]},{coord_list[x][1]}:"
        else:
            coord_str += f"{coord_list[x][0]},{coord_list[x][1]}"

    print(coord_str)
    return [coord_list, coord_str]


def get_entry(width: int, height: int, coords_42: list):
    while True:
        entry = tuple(
            (random.randint(0, width - 1), random.randint(0, height - 1))
        )
        found_same = False
        for coord in coords_42:
            if coord == entry:
                found_same = True
                break
        if found_same:
            continue
        return f"{entry[0]},{entry[1]}"


def get_exit(width: int, height: int, coords_42: list, entry: str):
    while True:
        exit = str(
            f"{random.randrange(1, width)},{random.randrange(1, height)}"
        )
        found_same = False
        for coord in coords_42:
            if coord == exit or exit == entry:
                found_same = True
                break
        if found_same:
            continue
        return exit


def generate_seed_config(seed: int):
    config = configparser.ConfigParser()
    random.seed(seed)
    width = random.randrange(4, 40)
    height = random.randrange(4, width)

    coords = set_42_coordinates(width, height)
    if coords is None:
        coord_42 = ""
        coords_list = []
    else:
        coords_list = coords[0]
        coord_42 = coords[1]

    entry = get_entry(width, height, coords_list)
    exit = get_exit(width, height, coords_list, entry)
    perfect = random.choice([True, False])
    output = "maze.txt"

    config['seed'] = {
        "SEED": seed
        }

    config['size'] = {
        "WIDTH": width,
        "HEIGHT": height,
        "ENTRY": entry,
        "EXIT": exit,
        "OUTPUT_FILE": output,
        "PERFECT": perfect,
        "42_COORDS": coord_42
    }

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


def main():
    set_42_coordinates(20, 20)


if __name__ == "__main__":
    main()
