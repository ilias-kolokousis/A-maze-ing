#!/usr/bin/env python3

import random
from src.maze_class import Maze
from src.viz import Viz, print_state, get_input
from src.solve_maze import solve_maze


def _produce_neighbors(maze: Maze, start: tuple) -> list[tuple]:
    """Produce a list of neighbor cells that we can continue on.
    It checks and eliminates any candidates that are outside of the
    grid or cells that belong in the '42' graphic.

    Args:
        maze (Maze): our maze object holding all the attributes for size
        start (tuple): the current cell we are on

    Returns:
        list[tuple]: all possible neighbors we can move into
    """
    x: int = start[0]
    y: int = start[1]
    candidates = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    if maze.coords_42 != (0, 0):
        return [(nx, ny) for nx, ny in candidates
                if nx >= 0 and nx < maze.width and ny >= 0 and ny < maze.height
                and (nx, ny) not in maze.coords_42]
    else:
        return [(nx, ny) for nx, ny in candidates
                if nx >= 0 and nx < maze.width
                and ny >= 0 and ny < maze.height]


def _carve_wall(maze: Maze, start: tuple[int],
                next_cell: tuple[int]) -> None:
    """Open up a path between two cells, i.e. converts the bit needed of
    the cell to 0. Bits are following this order, WSEN, and 1 means wall
    and 0 means no wall. It modifies the grid in-place.

    For example, if we have closed cell (0,0) (bits: 1111)
    moving to closed cell (0,1) (bits: 1111), it converts (0,0) to 1011
    and cell (0,1) to 1110.

    Args:
        maze (Maze): our maze object, needed for the grid and the
        attributes for opening up walls.
        start (tuple[int]): the current cell
        next_cell (tuple[int]): the cell we are moving into
    """
    if start[0] != next_cell[0]:
        dir: str = 'W' if start[0] - 1 == next_cell[0] else 'E'
    elif start[1] != next_cell[1]:
        dir: str = 'N' if start[1] - 1 == next_cell[1] else 'S'

    maze.grid[start[1]][start[0]] = maze.change_bit[dir](
        maze.grid[start[1]][start[0]])
    dir = maze.change_direction[dir]
    maze.grid[next_cell[1]][next_cell[0]] = maze.change_bit[dir](
        maze.grid[next_cell[1]][next_cell[0]])


def str_to_tuple(s: str) -> tuple:
    """Convert a string resembling a tuple to an actual
    tuple object

    Args:
        s (str): string to convert to tuple

    Returns:
        tuple[int, int]: converted string to tuple
    """
    lst = s.split(',')
    return (int(lst[0]), int(lst[1]))


def generate_prim(maze: Maze) -> None:
    """Utilise Prim's algorithm to generate a perfect maze"""
    visited: set[tuple] = {}

    try:
        visited = set(maze.coords_42)
    except TypeError:
        visited = set()
    visited.add(maze.entry)

    frontier = []
    for neighbor in _produce_neighbors(maze, maze.entry):
        if neighbor not in visited:
            frontier.append((neighbor, maze.entry))

    print("\033[2J\033[H", end="", flush=True)
    while frontier:
        index = random.randint(0, len(frontier) - 1)
        current, previous = frontier.pop(index)

        if current not in visited:
            _carve_wall(maze, previous, current)
            visited.add(current)

            for next_neighbor in _produce_neighbors(maze, current):
                if next_neighbor not in visited:
                    frontier.append((next_neighbor, current))
        print_state(maze)
    print_state(maze)

    grid: list[list[str]] = [row[:] for row in maze.grid]
    entry: str = f'{maze.entry[0]},{maze.entry[1]}'
    exit: str = f'{maze.exit[0]},{maze.exit[1]}'
    path: str = ''.join(solve_maze(maze))

    for row in range(maze.height):
        for cell in range(maze.width):
            grid[row][cell] = str(hex(maze.grid[row][cell]))[2:].upper()

    output: str = ''
    for row in grid:
        output += ''.join(row) + '\n'
    output += f'\n{entry}\n{exit}\n{path}'
    with open(maze.output_file, 'w') as f:
        f.write(output)

    print("\033[H", end="", flush=True)
    viz: Viz = Viz(maze.output_file, maze.coords_42)
    viz.render(viz.output)
    get_input(maze)


if __name__ == "__main__":
    generate_prim()
