import configparser
import OLD.conf_scripts.seed_config as sc


def create_custom_config():
    config = configparser.ConfigParser()
    x = input('Use default settings? (y/n)      ')
    if (x == 'y' or x == 'yes' or x == 'YES'):
        return
    elif (x == 'n' or x == 'no' or x == 'NO'):
        is_seed = input('Use a seed? (y/n)      ')
        if (is_seed == 'y' or is_seed == 'yes' or is_seed == 'YES'):
            seed = input('Seed:')
            if sc.is_valid_seed(seed) is True:
                width = sc.get_width(seed)
                height = sc.get_height(seed)
                entry = sc.get_entry(width, height, seed)
                exit = sc.get_exit(width, height, seed)
                perfect = sc.is_perfect(seed)
                output = input('Output file name: ') + ".txt"
            else:
                print("Invalid seed, proceeding without seed")
                seed = "None"
                width = input('Width: ')
                height = input('Height: ')
                entry = input('Entry coordinates (x,y): ')
                exit = input('Exit coordinates (x,y): ')
                output = input('Output file name: ') + ".txt"
                perfect = input('Perfect maze? (True/False) ')
        else:
            seed = "None"
            width = input('Width: ')
            height = input('Height: ')
            entry = input('Entry coordinates (x,y): ')
            exit = input('Exit coordinates (x,y): ')
            output = input('Output file name: ') + ".txt"
            perfect = input('Perfect maze? (True/False) ')
        config["CUSTOM"] = {
            "SEED": seed,
            "WIDTH": width,
            "HEIGHT": height,
            "ENTRY": entry,
            "EXIT": exit,
            "OUTPUT_FILE": output,
            "PERFECT": perfect
        }
    else:
        print("Wrong input, just write y or n")
    with open('./custom_config.ini', 'w') as configfile:
        config.write(configfile)


if __name__ == "__main__":
    create_custom_config()
