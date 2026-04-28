#!/usr/bin/env python3

import src.configuration as conf
from src.prims import generate_prim
from src.hunt_n_kill import generate_hunt_n_kill
from src.maze_class import Maze
import os
import sys


file_errors: tuple = (FileNotFoundError, PermissionError,
                      IsADirectoryError, OSError, UnicodeDecodeError)


class InsufficientArgs(Exception):
    """Custom exception. Inherits from Exception class"""
    pass


def handle_errors(config: dict[str, str | int | bool]) -> bool:
    """Handle errors for the following cases:
    1. Non integers in width and height
    2. Missing any of the mandatory keys
    3. Width or height is too big to create a nice maze
    4. Entry and exit doesn't contain integers.
    5. Entry and exit is not consisted by exactly two elements
       separated by a comma
    6. Perfect is not a boolean term
    7. Values inside entry and exit are outside of the maze borders
    8. Output file is unusable (for example, not permission)

    Args:
        config (dict[str, str  |  int  |  bool]): config dictionary of
                                                all the terms

    Raises:
        ValueError: If any error is raised, it is by convention a ValueError

    Returns:
        bool: True if no errors are raised, False if there's at least
            one error
    """
    required_keys: list[str] = [
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
            return False

    try:
        int(config['width'])
        int(config['height'])
    except ValueError:
        print(
            f"Error: 'width' and 'height' must be integers."
            f"\nGot '{config['width']}' and '{config['height']}'",
            file=sys.stderr
        )
        return False

    try:
        if (int(config['width']) * 2 * 2 > os.get_terminal_size().columns
           or int(config['height']) * 2 > os.get_terminal_size().lines):
            raise ValueError
    except ValueError:
        print("Error: Height and width is too big. It won't render correctly."
              "\nPlease put smaller values in or resize your terminal.",
              file=sys.stderr)
        return False

    if config['perfect'].lower() not in ('true', 'false'):
        print(
            f"Error: 'perfect' must be 'True' or 'False'."
            f"\nGot '{config['perfect']}", file=sys.stderr
        )
        return False

    try:
        entry: list[str, str] = config['entry'].split(',')
        exit: list[str, str] = config['exit'].split(',')
        [int(i) for i in entry]
        [int(i) for i in exit]
        if len(entry) != 2 or len(exit) != 2:
            raise ValueError
    except ValueError:
        print(
            "Error: Values inside the entry and exit must be bare integers "
            "and they must be exactly 2 each separated by a comma."
            f"\nGot '{config['entry']}' and '{config['exit']}'",
            file=sys.stderr)
        return False

    try:
        if not (0 <= int(entry[0]) < int(config['width'])
                and 0 <= int(exit[0]) < int(config['width'])
                and 0 <= int(entry[1]) < int(config['height'])
                and 0 <= int(exit[1]) < int(config['height'])):
            raise ValueError
    except ValueError:
        print(
            "Error: Values isnide entry and exit must be "
            f"between 0 and {config['width']} for the first value "
            f"of entry and exit and between 0 and {config['height']} "
            "for the second value of entry and exit"
            f"\nGot '{config['entry']}' and '{config['exit']}'",
            file=sys.stderr)
        return False

    try:
        with open(config['output_file'], 'w+') as f:
            f
    except file_errors as e:
        print("Error: Output file provided not valid:"
              f"\n{e}", file=sys.stderr)
        return False
    return True


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
                line: str = line.strip().lower()
                if '=' in line:
                    key, value = line.split('=', 1)
                    config[key.strip()] = value.strip()
    except file_errors as e:
        print(f"Error: {e}", file=sys.stderr)
        return

    if not handle_errors(config):
        return

    perfect: bool = config['perfect'].lower() == 'true'
    maze: Maze = Maze(config)

    if perfect:
        generate_prim(maze)
    else:
        generate_hunt_n_kill(maze)


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
