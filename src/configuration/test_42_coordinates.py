def plot_42(left: int, top: int):
    x = 1
    y = 0
    coords = []
    while x < 8:
        if x == 1 or 5 <= x <= 7:
            coords += [f"{x + left},{top - y}"]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if x == 1 or x == 7:
            coords += [f"{x + left},{top - y}"]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if 1 <= x <= 3 or 5 <= x <= 7:
            coords += [f"{x + left},{top - y}"]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if x == 3 or x == 5:
            coords += [f"{x + left},{top - y}"]
        x += 1
    x = 1
    y += 1
    while x < 8:
        if x == 3 or 5 <= x <= 7:
            coords += [f"{x + left},{top - y}"]
        x += 1
    return coords


def set_42_coordinates(width: int, height: int):
    if width < 9 or height < 7:
        return None

    pad_right = int((width - 7) / 2)
    if (width % 2) == 0:
        pad_left = pad_right + 1
    else:
        pad_left = pad_right
    print(f"Pad_right: {pad_right}")
    print(f"Pad_left: {pad_left}")

    pad_top = int((height - 5) / 2)
    if (height % 2) == 0:
        pad_bottom = pad_top + 1
    else:
        pad_bottom = pad_top
    print(f"Pad_top: {pad_top}")
    print(f"Pad_bottom: {pad_bottom}")

    coord_list = plot_42(pad_left, height - pad_top)
    coord_str = ""
    for x in range(len(coord_list)):
        if x != len(coord_list) - 1:
            coord_str += f"{coord_list[x]}:"
        else:
            coord_str += coord_list[x]
    print(coord_str)


def main():
    set_42_coordinates(9, 7)


if __name__ == "__main__":
    main()
