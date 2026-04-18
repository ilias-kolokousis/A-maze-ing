from configparser import ConfigParser
from prims import generate_prim


def choose_algo(fd: str):
    config_path = f"../src{fd}"
    print(config_path)
    config = ConfigParser()
    config.read(config_path)
    width = config.getint('size', 'width')
    height = config.getint('size', 'height')
    if config.get('size', 'perfect') == 'True':
        generate_prim(width, height, fd)
    else:
        print("generate with hunt-n-kill")
