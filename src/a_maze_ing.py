import configuration.configuration as config
import generate.generate as gen


def main():
    if config.generate_random_config():
        gen.generate_hex("./src/default_config.ini")
    else:
        gen.generate_hex("./src/custom_config.ini")


if __name__ == "__main__":
    main()
