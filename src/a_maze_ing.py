import configuration.configuration as conf
import prims as prims
import os
import sys


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
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.basename(fd)
    config_path = os.path.join(script_dir, filename)

    try:
        f = open(config_path, 'r')
    except FileNotFoundError:
        print(f"Error: Could not find config file '{config_path}'")
        return
    except PermissionError:
        print(f"Error: No permission to read file '{config_path}'")
        return

    config = {}
    with f:
        for line in f:
            line = line.strip().lower()
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()

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
            f"got '{config['width']}' and '{config['height']}"
        )
        return

    if config['perfect'] not in ('true', 'false'):
        print(
            f"Error: 'perfect' must be 'true' or 'false', "
            f"got '{config['perfect']}"
        )
        return

    perfect = config['perfect'] == 'true'

    if perfect:
        prims.generate_prim(width, height, config_path)
    else:
        print("generate with hunt-n-kill")


def main() -> None:
    """
    Main function
    """
    print(sys.argv[1])
    if conf.generate_random_config():
        choose_algo(f"./{sys.argv[1]}")
    else:
        choose_algo("./custom_config.txt")


if __name__ == "__main__":
    main()
