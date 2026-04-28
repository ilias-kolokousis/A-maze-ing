import random


def coord_str_to_tuple(s: str) -> tuple[int, int]:
    """Convert a string resembling a tuple to an actual
    tuple object

    Args:
        s (str): string to convert to tuple

    Returns:
        tuple[int, int]: converted string to tuple
    """
    lst = s.split(',')
    return (int(lst[0]), int(lst[1]))


def plot_42(left: int, top: int) -> list[tuple[int, int]]:
    """
    Calculates coordinates of the 42 cells

    Parameters
    ----------
    left : int
        The padding from the left side
    top : int
        The padding from the top side

    Returns
    -------
    list[tuple]
        returns a list of tuppels
          containing the x and y coordinates of each 42 cell
    """
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


CoordResult = tuple[list[tuple[int, int]], str]


def set_42_coords(width: int, height: int) -> CoordResult | None:
    """
    Calculates the padding on top and left, and calls
     the plot_42() function when 42 cells fit within maze size

    Parameters
    ----------
    width : int
        The width of the maze
    height : int
        The height of the maze

    Returns
    -------
    tuple[list[tuple], str]
        A tuple containing a list with tuples containing the 42
         cell coordinates, and a string representing the same coordinates
    None

    """
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

    return (coord_list, coord_str)


ListTuples = list[tuple[int, int]]


def get_entry(width: int, height: int, coords_42: ListTuples) -> str:
    """
    Randomizes a valid entry point within the maze boundaries,
     and outside of the 42 coordinates

    Parameters
    ----------
    width : int
        Width of the maze
    height : int
        Height of the maze
    coords_42 : list
        List of tuples containing coordinates of the 42 cells

    Returns
    -------
    str
        A string representation of the coordinates of the entry cell
    """
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


def get_exit(
        width: int, height: int,
        coords_42: list[tuple[int, int]], entry_str: str
        ) -> str:
    """
    Randomizes a valid exit point within the maze boundaries,
     and outside of the 42 coordinates and entry cell

    Parameters
    ----------
    width : int
        Width of the maze
    height : int
        Height of the maze
    coords_42 : list[tuple[int]]
        List of tuples containing coordinates of the 42 cells
    entry : str
        A string representation of the coordinates of the entry cell

    Returns
    -------
    str
        A string representation of the coordinates of the exit cell
    """
    while True:
        entry = coord_str_to_tuple(entry_str)
        exit = tuple(
            (random.randint(0, width - 1), random.randint(0, height - 1))
        )
        found_same = False
        for coord in coords_42:
            if coord == exit or exit == entry:
                found_same = True
                break
        if found_same:
            continue
        return f"{exit[0]},{exit[1]}"


def generate_seed_config(seed: int) -> None:
    """Generates a random config file using a seed

    Parameters
    ----------
    seed : int
        Seed to be used in randomization
    """
    random.seed(seed)
    width: int = random.randrange(4, 40)
    height: int = random.randrange(4, width)
    coords: CoordResult | None = set_42_coords(width, height)

    if coords is None:
        coords_list: list = []
    else:
        coords_list = coords[0]

    entry: str = get_entry(width, height, coords_list)
    exit: str = get_exit(width, height, coords_list, entry)
    perfect: bool = random.choice([True, False])
    output: str = "output.txt"

    try:
        with open('custom_config.txt', 'w') as f:
            f.write(f"seed = {seed}\n")
            f.write(f"width = {width}\n")
            f.write(f"height = {height}\n")
            f.write(f"entry = {entry}\n")
            f.write(f"exit = {exit}\n")
            f.write(f"output_file = {output}\n")
            f.write(f"perfect = {perfect}\n")
    except PermissionError:
        print("Error: No permission to write to './custom_config.txt'")
        return
    except OSError as e:
        print(f"Error: Could not write config file: {e}")
        return


def generate_random_config() -> bool:
    """Takes the user input, and generates a desired config file

    Returns
    -------
    bool
        returns True when default settings should be used,
         and False when a custom config file should be used
    """
    x: str = input('Use default settings? (y/n)      ')
    if (x == 'y' or x == 'yes' or x == 'YES'):
        return True
    elif (x == 'n' or x == 'no' or x == 'NO'):
        is_seed: str = input('Use a seed? (y/n)      ')
        if (is_seed == 'y' or is_seed == 'yes' or is_seed == 'YES'):
            valid_seed: bool = False

            # Get seed. If input is invalid, try 2 more times
            # to get valid input. In the last try, produce a random seed.

            for i in range(3):
                try:
                    seed: int = int(input('Seed:'))
                    if seed == 999999999 or not seed:
                        return True
                    valid_seed = True
                    break
                except ValueError as e:
                    print(f"Seed needs to be an integer: {e}")
                    print(f"Try {i + 1}/3")
                    if i == 2:
                        print("Continuing with random seed...")
            if valid_seed:
                generate_seed_config(seed)
            else:
                seed = random.randint(0, 999999999999999999)
                generate_seed_config(seed)
        elif (
            is_seed == 'n' or
            is_seed == 'no' or is_seed == 'NO'
        ):
            seed = random.randint(0, 999999999999999999)
            generate_seed_config(seed)
        else:
            go_again: str = input(
                                  'Could not understand your input,'
                                  'do you want to retry? (y/n)'
                                )
        if (go_again == 'y' or go_again == 'yes' or go_again == 'YES'):
            generate_random_config()
        else:
            exit()
        return False
    else:
        go_again = input(
            'Could not understand your input, do you want to retry? (y/n)'
        )
        if (go_again == 'y' or go_again == 'yes' or go_again == 'YES'):
            generate_random_config()
        else:
            exit()
    return False
