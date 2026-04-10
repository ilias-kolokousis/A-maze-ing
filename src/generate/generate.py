import configparser


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

    print(seed)
    print(width)
    print(height)
    print(entry)
    print(exit)
    print(output_file)
    print(perfect)
