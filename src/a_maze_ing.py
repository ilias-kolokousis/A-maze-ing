import configuration.configuration as conf
from configparser import ConfigParser
import prims as prims
import os
import sys


def choose_algo(fd: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.basename(fd)
    config_path = os.path.join(script_dir, filename)

    config = ConfigParser()
    file = config.read(config_path)
    if not file:
        raise FileNotFoundError(f"Could not open file: {fd}")

    width = config.getint('size', 'width')
    height = config.getint('size', 'height')
    if config.get('size', 'perfect') == 'True':
        prims.generate_prim(width, height, sys.argv[1])
    else:
        print("generate with hunt-n-kill")


def main():
    if conf.generate_random_config():
        choose_algo(f"./{sys.argv[1]}")
    else:
        choose_algo("./custom_config.ini")


if __name__ == "__main__":
    main()
