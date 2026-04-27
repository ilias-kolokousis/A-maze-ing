#!/usr/bin/env python3

from src.maze_class import Maze


class Node():
    def __init__(self, current_cell: tuple[int, int], g: int = 0,
                 h: int = 0, parent: tuple[int, int] = None) -> None:
        self.current_cell: tuple[int, int] = current_cell
        self.g: int = g
        self.h: int = h
        self.parent: tuple[int, int] = parent

    @property
    def f(self) -> int:
        return self.g + self.h


def find_direction(curr_cell: tuple[int, int],
                   neighbor: tuple[int, int]) -> str:
    if curr_cell[0] != neighbor[0]:
        return 'W' if curr_cell[0] - 1 == neighbor[0] else 'E'
    elif curr_cell[1] != neighbor[1]:
        return 'N' if curr_cell[1] - 1 == neighbor[1] else 'S'


def is_blocked(maze: Maze, curr_cell: tuple[int, int],
               neighbor: tuple[int, int]) -> bool:
    direction: str = find_direction(curr_cell, neighbor)
    cell: int = int(maze.grid[curr_cell[1]][curr_cell[0]])

    if direction == 'N':
        return (cell & 0b0001)
    elif direction == 'E':
        return (cell & 0b0010)
    elif direction == 'S':
        return (cell & 0b0100)
    elif direction == 'W':
        return (cell & 0b1000)


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


def solve_maze(maze: Maze) -> list[tuple]:
    h: int = (abs(maze.exit[0] - maze.entry[0])
              + abs(maze.exit[1] - maze.entry[1]))
    open: dict[tuple[int, int], Node] = {maze.entry: Node(maze.entry, h=h)}
    closed: dict[tuple[int, int], Node] = {}

    while 1 == 1:
        lowest_f_node: Node = open[list(open.keys())[0]]
        for node in open:
            if open[node].f < lowest_f_node.f:
                lowest_f_node = open[node]
            elif (open[node].f == lowest_f_node.f
                  and open[node].g > lowest_f_node.g):
                lowest_f_node = open[node]

        closed.update({lowest_f_node.current_cell: lowest_f_node})
        del open[lowest_f_node.current_cell]
        current: tuple[int, int] = lowest_f_node.current_cell
        if current == maze.exit:
            break
        prob_neigh: list = _produce_neighbors(maze, lowest_f_node.current_cell)
        neighbors: list = []
        for n in prob_neigh:
            if (n not in closed
               and not is_blocked(maze, lowest_f_node.current_cell, n)):
                neighbors.append(n)

        for n in neighbors:
            tent_g: int = lowest_f_node.g + 1
            nodes: list[tuple] = [open[node].current_cell for node in open]
            h: int = abs(maze.exit[0] - n[0]) + abs(maze.exit[1] - n[1])
            node: Node = Node(n, tent_g, h, current)
            if n not in nodes:
                open.update({node.current_cell: node})
            else:
                if tent_g < open[n].g:
                    open[n].g = tent_g
                    open[n].parent = current

    path: list[tuple[int, int]] = [current]
    while path[-1] != maze.entry:
        path.append(lowest_f_node.parent)
        lowest_f_node = closed[lowest_f_node.parent]
    path.reverse()
    path_dir: list[str] = []
    for cell in range(len(path) - 1):
        path_dir.append(find_direction(path[cell], path[cell + 1]))
    return path_dir


if __name__ == "__main__":
    print(is_blocked())
