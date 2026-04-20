#!/usr/bin/env python3

import random
from maze_class import Maze
from solve_maze import solve_maze


def _get_x_y(maze: Maze) -> tuple[int]:
    """Create a tuple with random values in the limits of our grid
    to start creating the maze.

    Args:
        maze (Maze): our maze object holding all the attributes for size

    Returns:
        tuple[int]: a random point inside the grid. The order signifies
        x and y respectively.
    """
    x: int = random.randint(0, maze.width - 1)
    y: int = random.randint(0, maze.height - 1)
    return (x, y)


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
    return [(nx, ny) for nx, ny in candidates
            if nx >= 0 and nx < maze.width and ny >= 0 and ny < maze.height
            and (nx, ny) not in maze.coords_42]


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


def _hunt(maze: Maze, start: tuple[int], visited: set[tuple]) -> tuple:
    """Part of the hunt and kill process. Find an invisited cell when we have
    exhausted the possible neighbors we can move into and we need to hunt an
    unvisited cell.

    Args:
        maze (Maze): our maze object holding useful attributes, like
        grid and size
        start (tuple[int]): the current cell
        visited (set[tuple]): the list of the cells visited already

    Returns:
        tuple: the coordinates to start new carving
    """
    neighbors: list[tuple] = _produce_neighbors(maze, start)
    cell_found: bool = False
    for row in range(maze.height):
        for cell in range(maze.width):
            if ((cell, row) not in visited
                and (cell, row) not in maze.coords_42
                and any(n in visited
                        for n
                        in _produce_neighbors(maze, (cell, row)))):
                start = (cell, row)
                neighbors = _produce_neighbors(maze, start)
                cell_found = True
                break
        if cell_found:
            break

    next_cell: tuple[int] = random.choice(neighbors)
    while next_cell not in visited:
        next_cell = random.choice(neighbors)
    visited.add(start)
    _carve_wall(maze, start, next_cell)
    return start


def _kill(maze: Maze, start: tuple, visited: set[tuple]) -> tuple:
    """Part of the hunt and kill algorithm. It opens up paths by "killing"
    unvisited neighbor cells.

    Args:
        maze (Maze): maze object
        start (tuple): the current cell
        visited (set[tuple]): the list of the cells visited already

    Returns:
        tuple: the next cell coordinates
    """
    neighbors: list[tuple] = _produce_neighbors(maze, start)
    next_cell: tuple[int] = random.choice(neighbors)
    if all(n in visited for n in neighbors):
        return start
    if random.choices([False, True], weights=(50, 50), k=1)[0]:
        while next_cell in visited:
            next_cell = random.choice(neighbors)
    _carve_wall(maze, start, next_cell)
    visited.add(next_cell)
    return next_cell


def create_maze() -> None:
    """The main logic behind the hunt and kill algorithm. It first
    initializes the maze object. Then, it finds a random start in the grid
    and starts 'killing' (carving walls) until there is no unvisited
    neighbor. In that case, it either finishes (if all cells have been
    visited) or finds a cell that is unvisited and starts from there
    carving new walls.
    """
    maze: Maze = Maze('custom_config.ini')
    start: tuple[int] = _get_x_y(maze)
    while start in maze.coords_42:
        start = _get_x_y(maze.width - 1, maze.height - 1)
    visited: set[tuple] = {start}

    while len(visited) + len(maze.coords_42) < maze.width * maze.height:
        neighbors: list[tuple] = _produce_neighbors(maze, start)

        if all(n in visited for n in neighbors):
            start = _hunt(maze, start, visited)
        start = _kill(maze, start, visited)

    print(solve_maze(maze))
    for row in range(maze.height):
        for cell in range(maze.width):
            maze.grid[row][cell] = str(hex(maze.grid[row][cell]))[2:].upper()
    output = ''
    for row in maze.grid:
        output += ''.join(row) + '\n'
    with open(maze.output_file, 'w') as f:
        f.write(output)


if __name__ == "__main__":
    create_maze()
