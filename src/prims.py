import random
from typing import Callable
from configuration import configuration as conf


def grid_init(width: int, height: int) -> list[list[int]]:
    """Initiates the grid and filling it up with the integer
    representation of binary 1111

    Parameters
    ----------
    width : int
        Width of the maze
    height : int
        Height of the maze

    Returns
    -------
    list[list[int]]
        Initiated grid
    """
    grid: list[list[int]] = []
    for index_y in range(height):
        grid.append([])
        for index_x in range(width):
            grid[index_y].append(15)
    print(grid)
    return grid


change_bit: dict[str, Callable[[int], int]] = {
    'W': lambda x: x & ~(1 << 3),
    'E': lambda x: x & ~(1 << 1),
    'S': lambda x: x & ~(1 << 2),
    'N': lambda x: x & ~(1 << 0)
}

change_direction: dict[str, str] = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}


CrdTup = tuple[int, int]
GridList = list[list[int]]


def set_neighbors(current: CrdTup, width: int, height: int) -> list[CrdTup]:
    """Finds all neighbors of the current cell

    Parameters
    ----------
    current : CrdTup
        The newest cell that has been added to the maze
    width : int
        Width of the maze
    height : int
        Height of the maze

    Returns
    -------
    list[CrdTup]
        List of tuples with all new neighbors
    """
    x: int = current[0]
    y: int = current[1]
    candidates = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return [(nx, ny) for nx, ny in candidates
            if nx >= 0 and nx < width and ny >= 0 and ny < height]


def carve_wall(grid: GridList, cur: CrdTup,
               next_n: CrdTup) -> tuple[list[list[int]], CrdTup]:
    """'Carves' a wall between the current cell and the new cell
         by updating the hex value in the grid

    Parameters
    ----------
    grid : GridList
        The grid
    cur : CrdTup
        The current cell
    next_n : CrdTup
        The neighboring cell the current cell will connect to

    Returns
    -------
    tuple[list[list[int]], CrdTup]
        Returns a tuple containing the updated grid,
         as well as the new current cell
    """
    if cur[0] != next_n[0]:
        dir: str = 'W' if cur[0] - 1 == next_n[0] else 'E'
    elif cur[1] and cur[1] != next_n[1]:
        dir = 'N' if cur[1] - 1 == next_n[1] else 'S'

    grid[cur[1]][cur[0]] = change_bit[dir](grid[cur[1]][cur[0]])
    dir = change_direction[dir]
    grid[next_n[1]][next_n[0]] = change_bit[dir](grid[next_n[1]][next_n[0]])
    return (grid, cur)


def generate_prim(width: int, height: int, fd: str) -> None:
    """Utilises Prim's algorithm to generate a perfect maze

    Parameters
    ----------
    width : int
        Width of the maze
    height : int
        Height of the maze
    fd : str
        Config file file descriptor
    """
    f = open(fd, 'r')

    config = {}
    with f:
        for line in f:
            line = line.strip().lower()
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

    try:
        if 'seed' not in config:
            seed = 999999999
        else:
            seed = int(config['seed'])
    except ValueError:
        print(f"Error: 'seed' must be an integer, got '{config['seed']}'")
        return

    try:
        start_cell = conf.coord_str_to_tuple(config['entry'])
    except (ValueError, TypeError):
        print(f"Error: 'entry' has an invalid format, got '{config['entry']}'")
        return

    if not (0 <= start_cell[0] < width and 0 <= start_cell[1] < height):
        print(
            f"Error: Entry point {start_cell} is out of "
            f"bounds for maze of size {width}x{height}"
        )
        return

    grid: list[list[int]] = grid_init(width, height)

    try:
        coords = conf.set_42_coords(width, height)
        if coords is not None:
            visited = set(coords[0])
    except TypeError:
        visited = set()

    visited.add(start_cell)

    frontier = []
    for neighbor in set_neighbors(start_cell, width, height):
        if neighbor not in visited:
            frontier.append((neighbor, start_cell))

    random.seed(seed)
    while frontier:
        index = random.randint(0, len(frontier) - 1)
        current, previous = frontier.pop(index)
        if current not in visited:
            grid, _ = carve_wall(grid, previous, current)
            visited.add(current)
            for next_neighbor in set_neighbors(current, width, height):
                if next_neighbor not in visited:
                    frontier.append((next_neighbor, current))

    str_grid: list[list[str]] = []
    for row in range(height):
        inner: list[str] = []
        for cell in range(width):
            inner.append(str(hex(grid[row][cell]))[2:].upper())
        str_grid.append(inner)

    output = ''
    for str_row in str_grid:
        output += ''.join(str_row) + '\n'

    output_file = config['output_file']
    try:
        with open(output_file, 'w') as f:
            f.write(output)
    except PermissionError:
        print(f"Error: No permission to write to '{output_file}'")
        return
    except OSError as e:
        print(f"Error: Could not write {output_file}: {e}")
        return
