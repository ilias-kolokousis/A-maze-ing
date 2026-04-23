import random
from configparser import ConfigParser
from configuration import configuration as conf


def get_x_y(width: int, height: int) -> tuple[int]:
    x: int = random.randint(0, width)
    y: int = random.randint(0, height)
    return (x, y)


def grid_init(width: int, height: int) -> list[list[int]]:
    grid: list[list[int]] = []
    for index_y in range(height):
        grid.append([])
        for index_x in range(width):
            grid[index_y].append(15)
    print(grid)
    return grid


change_bit: dict = {'W': lambda x: x & ~(1 << 3),
                    'E': lambda x: x & ~(1 << 1),
                    'S': lambda x: x & ~(1 << 2),
                    'N': lambda x: x & ~(1 << 0)}

change_direction: dict = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}


def produce_neighbors(start: tuple, width: int, height: int) -> list[tuple]:
    x: int = start[0]
    y: int = start[1]
    candidates = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    return [(nx, ny) for nx, ny in candidates
            if nx >= 0 and nx < width and ny >= 0 and ny < height]


def carve_wall(grid: list[list], start: tuple[int],
               next_n: tuple[int]) -> list[list]:
    if start[0] != next_n[0]:
        dir: str = 'W' if start[0] - 1 == next_n[0] else 'E'
    elif start[1] != next_n[1]:
        dir: str = 'N' if start[1] - 1 == next_n[1] else 'S'

    grid[start[1]][start[0]] = change_bit[dir](grid[start[1]][start[0]])
    dir = change_direction[dir]
    grid[next_n[1]][next_n[0]] = change_bit[dir](grid[next_n[1]][next_n[0]])
    return [grid, start]


def str_to_tuple(s: str) -> tuple:
    lst = s.split(',')
    return (int(lst[0]), int(lst[1]))


def generate_prim(width: int, height: int, fd: str):
    config = ConfigParser()

    file = config.read(fd)

    if not file:
        raise FileNotFoundError(f"Configuration file not found: {fd}")

    start: tuple[int] = get_x_y(width - 1, height - 1)
    grid: list[list[int]] = grid_init(width, height)
    visited: set[tuple] = {start}

    grid = grid_init(width, height)

    try:
        visited = set(conf.set_42_coordinates(width, height)[0])
    except TypeError:
        visited = set()
    start_cell = str_to_tuple(config.get('size', 'entry'))
    visited.add(start_cell)

    frontier = []
    for neighbor in produce_neighbors(start_cell, width, height):
        if neighbor not in visited:
            frontier.append((neighbor, start_cell))

    seed = int(config.getint('seed', 'seed'))
    random.seed(seed)

    while frontier:
        index = random.randint(0, len(frontier) - 1)
        current, previous = frontier.pop(index)

        if current not in visited:
            grid, _ = carve_wall(grid, previous, current)
            visited.add(current)

            for next_neighbor in produce_neighbors(current, width, height):
                if next_neighbor not in visited:
                    frontier.append((next_neighbor, current))

    for row in range(height):
        for cell in range(width):
            grid[row][cell] = str(hex(grid[row][cell]))[2:].upper()

    output = ''
    for row in grid:
        output += ''.join(row) + '\n'
    with open('output.txt', 'w') as f:
        f.write(output)
