import random
from src.hunt_n_kill import print_state
from src.maze_class import Maze
from src.viz import render, create_grid
from src.solve_maze import solve_maze


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


CrdTup = tuple[int, int]
GridList = list[list[int]]


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
            if nx >= 0 and nx < maze.width and ny >= 0 and ny < maze.height]


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
    
    #######################################################

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
