#!/usr/bin/env python3

import random
from configparser import ConfigParser
from typing import List, Callable, TypeAlias

BitOp: TypeAlias = Callable[[int], int]


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

    def __init__(self, config_path: str) -> None:
        """Initialization of a Maze object. Can be used instead of accessing
        the config file everytime. Initiliazes also a grid.

        Args:
            config_path (str): path to the config.ini file
        """
        config: ConfigParser = ConfigParser()
        config.read(config_path)
        self.seed: int = config.getint('custom', 'seed')
        if self.seed is not None:
            random.seed(self.seed)
        self.width: int = config.getint('custom', 'width')
        self.height: int = config.getint('custom', 'height')
        self.entry: tuple[int, ...] = tuple(
            int(x) for x in config.get('custom', 'entry').split(','))
        self.exit: tuple[int, ...] = tuple(
            int(x) for x in config.get('custom', 'exit').split(','))
        self.output_file: str = config.get('custom', 'output_file')
        self.perfect: bool = config.getboolean('custom', 'perfect')
        self.coords_42: List[tuple[int, ...]] = [tuple(int(x)
                                                 for x in pair.split(','))
                                                 for pair in config.get(
                                                     'custom', '42_coords')
                                                 .split(':')]
        self.grid: list[list[int]] = [[15 for w in range(self.width)]
                                      for h in range(self.height)]


if __name__ == '__main__':
    maze: Maze = Maze('src/custom_config.ini')
    for key, value in maze.__dict__.items():
        if key == 'grid':
            initialized: bool = all(all(x == 15 for x in i) for i in value)
            correct_size: bool = (len(value) == maze.height
                                  and all(len(x) == maze.width
                                          for x in value))
            print(f'Grid initialized and correct size: {initialized
                                                        and correct_size}')
        else:
            print(f'{key}: {value}')
