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
