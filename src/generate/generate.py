import configparser


def str_to_list(s: str, sep: str):
    x = 0
    current = ""
    new_list = []
    while x < len(s):
        if s[x] == sep:
            new_list += [current]
            current = ""
            x += 1
        else:
            current += s[x]
            x += 1
    return new_list


def generate_hex(fd: str):
    config = configparser.ConfigParser()
    config.read(fd)
    section = config.sections()[0]

    seed = int(config[section]['SEED'])
    width = int(config[section]['WIDTH'])
    height = int(config[section]['HEIGHT'])
    entry = config[section]['ENTRY']
    exit = config[section]['EXIT']
    output_file = config[section]['OUTPUT_FILE']
    perfect = config[section]['PERFECT']
    coord_42 = str_to_list(config[section]['42_coords'], ':')

    print(seed)
    print(width)
    print(height)
    print(entry)
    print(exit)
    print(output_file)
    print(perfect)
    print(coord_42)
