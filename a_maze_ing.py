#!/usr/bin/env python3

import src.configuration as conf
import src.primsI as primsI
from src.hunt_n_kill import create_maze
from src.maze_class import Maze, tester
import os
import sys


file_errors: tuple = (FileNotFoundError, PermissionError,
                      IsADirectoryError, OSError, UnicodeDecodeError)


class InsufficientArgs(Exception):
    """Custom exception. Inherits from Exception class"""
    pass


def choose_algo(fd: str) -> None:
    """
    Checks for errors, and when none are found, decides on the
     algorithm to use. When the perfect key is true, it uses
     prims algorithm. Otherwise it uses hunt-n-kill algorithm

    Parameters
    ----------
    fd : str
        Config file file descriptor
    """
    script_dir: str = os.path.dirname(os.path.abspath(__file__))
    filename: str = os.path.basename(fd)
    config_path = os.path.join(script_dir, filename)

    try:
        with open(config_path, 'r') as f:
            config: dict[str, str | int | bool] = {}
            for line in f:
                line = line.strip().lower()
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except file_errors as e:
        print(f"Error: {e}", file=sys.stderr)
        return

    required_keys = [
        'width',
        'height',
        'entry',
        'exit',
        'output_file',
        'perfect'
    ]
    for key in required_keys:
        if key not in config:
            print(f"Error: Missing required field '{key}' in config file")
            return

    try:
        width: int = int(config['width'])
        height: int = int(config['height'])
    except ValueError:
        print(
            f"Error: 'width' and 'height' must be integers, "
            f"got '{config['width']}' and '{config['height']}",
            file=sys.stderr
        )
        return

    if config['perfect'] not in ('true', 'false'):
        print(
            f"Error: 'perfect' must be 'true' or 'false', "
            f"got '{config['perfect']}", file=sys.stderr
        )
        return

    perfect = config['perfect'] == 'true'
    maze: Maze = Maze(config)

    if perfect:
        primsI.generate_prim(width, height, config_path)
    else:
        create_maze(maze)  # hunt-n-kill algo


def main() -> None:
    """Main function"""
    try:
        if len(sys.argv) > 2:
            raise InsufficientArgs
        else:
            if conf.generate_random_config():
                if len(sys.argv) != 2:
                    raise InsufficientArgs
                else:
                    choose_algo(f"./{sys.argv[1]}")
            else:
                choose_algo("./custom_config.txt")
    except InsufficientArgs:
        print(f"{len(sys.argv) - 1} have been provided."
              " 1 argument is needed."
              "\nRun:"
              "\n./a_maze_ing.py config.txt", file=sys.stderr)


if __name__ == "__main__":
    main()
