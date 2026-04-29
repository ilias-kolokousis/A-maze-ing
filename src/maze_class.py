#!/usr/bin/env python3

import random
from typing import Callable, TypeAlias
from src.configuration import plot_42

BitOp: TypeAlias = Callable[[int], int]


class EntryExitInFortyTwo(Exception):
    pass


class Maze():
    """Maze object. Bares as attributes the info we get from the cconfig.ini
    file, along with a grid initialization and useful dictionaries to create
    a maze.

    change_bit: It compares two cells and depending on the direction it open up
    a wall by setting that bit to 0.

    change_direction: Because when we open up one wall in one direction, we
    need to do the same for the cell we are going into, but for the opposite
    side.
    """
    change_bit: dict[str, BitOp] = {'W': lambda x: x & ~(1 << 3),
                                    'E': lambda x: x & ~(1 << 1),
                                    'S': lambda x: x & ~(1 << 2),
                                    'N': lambda x: x & ~(1 << 0)}

    change_direction: dict[str, str] = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

    def __init__(self, config: dict) -> None:
        """Initialization of a Maze object. Can be used instead of accessing
        the config file everytime. Initiliazes also a grid.

        Args:
            config_path (str): path to the config.ini file
        """
        try:
            seed_val = config.get('seed')
            if seed_val is None:
                raise ValueError
            self.seed: int | None = int(seed_val)
        except ValueError:
            self.seed = None
        if self.seed is not None:
            random.seed(int(self.seed))
        self.width: int = int(config['width'])
        self.height: int = int(config['height'])
        parts = config['entry'].split(',')
        self.entry: tuple[int, int] = (int(parts[0]), int(parts[1]))
        parts = config['exit'].split(',')
        self.exit: tuple[int, int] = (int(parts[0]), int(parts[1]))
        self.output_file: str = config['output_file']
        self.perfect: bool = config['perfect'].lower() == 'true'
        self.grid: list[list[int]] = [[15 for w in range(self.width)]
                                      for h in range(self.height)]

    @property
    def coords_42(self) -> list[tuple[int, int]] | None:
        """Set the coordinates for the 42 graphic

        Returns:
            list[tuple[int, ...]] | None: a list of coordinates. None if
            the maze is too small for 42 to fit
        """
        if self.width < 9 or self.height < 7:
            return None

        pad_left: int = (self.width - 8) // 2
        pad_top: int = (self.height - 5) // 2

        graphic: list[tuple[int, int]] = plot_42(pad_left, pad_top)
        if self.entry in graphic or self.exit in graphic:
            return None
        return graphic

    def grid_init(self) -> None:
        """Initiliaze the grid if needed"""
        self.grid = [[15 for w in range(self.width)]
                     for h in range(self.height)]


def tester(maze: Maze) -> None:
    """Test if all the Maze attributes have been correctly
    initialized. Used for debugging.

    Args:
        maze (Maze): Maze object
    """
    for key, value in maze.__dict__.items():
        if key == 'grid':
            initialized: bool = all(all(x == 15 for x in i) for i in value)
            correct_size: bool = (len(value) == maze.height
                                  and all(len(x) == maze.width
                                          for x in value))
            print("Grid initialized and"
                  f" correct size: {initialized and correct_size}")
        else:
            print(f'{key}: {value}')
    print(f'coords_42: {maze.coords_42}')


if __name__ == '__main__':
    print()
