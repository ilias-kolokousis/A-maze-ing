#!/usr/bin/env python3

import random
from configparser import ConfigParser


# random.seed(5)


def get_x_y(width: int, height: int) -> tuple[int]:
    x: int = random.randint(0, width)
    y: int = random.randint(0, height)
    return (x, y)


config_filepath: str = 'test_config.ini'

config: ConfigParser = ConfigParser()
file: list = config.read(config_filepath)
width: int = config.getint('DEFAULT', 'width')
height: int = config.getint('DEFAULT', 'height')
start: tuple[int] = get_x_y(width - 1, height - 1)


def grid_init(width: int, height: int) -> list[list[int]]:
    grid: list[list[int]] = []
    for h_length in range(height):
        grid.append([])
        for w_length in range(width):
            grid[h_length].append(15)
    return grid


grid: list[list[int]] = grid_init(width, height)
visited: set[tuple] = {start}

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


def hunt(grid: list[list], start: tuple[int]) -> list[list]:
    neighbors: list[tuple] = produce_neighbors(start, width, height)
    cell_found: bool = False
    for row in range(height):
        for cell in range(width):
            if ((cell, row) not in visited
                and any(n in visited
                        for n
                        in produce_neighbors((cell, row), width, height))):
                start = (cell, row)
                neighbors = produce_neighbors(start, width, height)
                cell_found = True
                break
        if cell_found:
            break

    next_n: tuple[int] = random.choice(neighbors)
    while next_n not in visited:
        next_n = random.choice(neighbors)
    visited.add(start)
    return carve_wall(grid, start, next_n)


def kill(grid: list[list], start: tuple) -> list:
    neighbors: list[tuple] = produce_neighbors(start, width, height)
    next_n: tuple[int] = random.choice(neighbors)
    if all(n in visited for n in neighbors):
        return [grid, start]
    while next_n in visited:
        next_n = random.choice(neighbors)
    res: list = carve_wall(grid, start, next_n)
    start = next_n
    visited.add(next_n)
    return [res[0], start]


while len(visited) < width * height:
    neighbors: list[tuple] = produce_neighbors(start, width, height)

    if all(n in visited for n in neighbors):
        res: list = hunt(grid, start)
        grid = res[0]
        start = res[1]

    res: list = kill(grid, start)
    grid = res[0]
    start = res[1]


if __name__ == "__main__":
    for row in range(height):
        for cell in range(width):
            grid[row][cell] = str(hex(grid[row][cell]))[2:].upper()
    output = ''
    for row in grid:
        output += ''.join(row) + '\n'
    with open('output.txt', 'w') as f:
        f.write(output)
