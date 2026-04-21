#!/usr/bin/env python3

COLORS: dict[str, str] = {'Black': '\033[40m \033[0m',
                          'Red': '\033[41m \033[0m',
                          'Green': '\033[42m \033[0m',
                          'Yellow': '\033[43m \033[0m',
                          'Blue': '\033[44m \033[0m',
                          'Purple': '\033[45m \033[0m',
                          'Cyan': '\033[46m \033[0m',
                          'White': '\033[47m \033[0m'}
HEX_TO_BIN: dict[str, str] = {'0': '0000',
                              '1': '0001',
                              '2': '0010',
                              '3': '0011',
                              '4': '0100',
                              '5': '0101',
                              '6': '0110',
                              '7': '0111',
                              '8': '1000',
                              '9': '1001',
                              'A': '1010',
                              'B': '1011',
                              'C': '1100',
                              'D': '1101',
                              'E': '1110',
                              'F': '1111'}


def interchange_list_element(src_lst: list,
                             element: str | list, size: int) -> list:
    output: list = []
    i: int = 0
    for row in range(size * 2):
        if row % 2 == 0:
            output.append(element)
        else:
            output.append(src_lst[i])
            i += 1
    output.append(element)
    return output


def create_paths_in_rows(output: list[list[str]],
                         width: int) -> list[list[str]]:
    for row in range(len(output)):
        if row % 2 == 0:
            visual_width = width * 2
            output[row] = ['wall'] * (visual_width + 1)
        else:
            for cell in range(len(output[row])):
                if output[row][cell] not in HEX_TO_BIN:
                    continue
                encoding: list = list(HEX_TO_BIN[output[row][cell]])
                if encoding[2] == '0':
                    output[row][cell + 1] = 'path'
    return output


def create_paths_in_columns(output: list[list[str]]) -> list[list[str]]:
    for row in range(len(output)):
        for cell in range(len(output[row])):
            if output[row][cell] not in HEX_TO_BIN:
                continue
            encoding: list = list(HEX_TO_BIN[output[row][cell]])
            if encoding[1] == '0':
                output[row + 1][cell] = 'path'
            if output[row][cell] != 'wall':
                output[row][cell] = 'path'
    return output


def create_walls_and_paths(maze: str, width: int,
                           height: int) -> list[list[str]]:
    maze_lst: list = [interchange_list_element(list(row), 'wall', width)
                      for row in maze.split('\n')[:-4]]
    output: list = interchange_list_element(maze_lst, ['wall'], height)
    output = create_paths_in_rows(output, width)
    output = create_paths_in_columns(output)
    return output


def create_solution_path(start: tuple[int, int],
                         path: str, output: list) -> list[list[str]]:
    current_cell: tuple = start[:]
    for direction in path:
        if direction == 'N':
            current_cell = current_cell[0], current_cell[1] - 2
            output[current_cell[1] + 1][current_cell[0]] = 'solved'
        elif direction == 'S':
            current_cell = current_cell[0], current_cell[1] + 2
            output[current_cell[1] - 1][current_cell[0]] = 'solved'
        elif direction == 'E':
            current_cell = current_cell[0] + 2, current_cell[1]
            output[current_cell[1]][current_cell[0] - 1] = 'solved'
        elif direction == 'W':
            current_cell = current_cell[0] - 2, current_cell[1]
            output[current_cell[1]][current_cell[0] + 1] = 'solved'
        output[current_cell[1]][current_cell[0]] = 'solved'
    return output


def create_grid() -> list[list[str]]:
    OUTPUT_PATH: str = 'maze.txt'
    with open(OUTPUT_PATH, 'r') as f:
        maze: str = f.read()

    WIDTH: int = len(maze.split('\n')[0])
    HEIGHT: int = len(maze.split('\n')[:-3]) - 1
    start_raw: tuple = tuple(int(i) for i in maze.split('\n')[-3].split(','))
    end_raw: tuple = tuple(int(i) for i in maze.split('\n')[-2].split(','))
    path: str = maze.split('\n')[-1]

    output: list = create_walls_and_paths(maze, WIDTH, HEIGHT)

    actual_start: tuple = (int(start_raw[0]) * 2 + 1,
                           int(start_raw[1]) * 2 + 1)
    actual_end: tuple = (int(end_raw[0]) * 2 + 1, int(end_raw[1]) * 2 + 1)

    output = create_solution_path(actual_start, path, output)

    output[actual_start[1]][actual_start[0]] = 'start'
    output[actual_end[1]][actual_end[0]] = 'end'
    return output


def get_input():
    print("=== A-Maze-ing ===")
    print(" 1. Regenerate new maze")
    print(" 2. Show/Hide path from entry to exit")
    


def render(grid) -> None:
    CELL_COLORS = {
        'wall':   '\033[47m',
        'path':   '\033[40m',
        'start':  '\033[45m',
        'end':    '\033[44m',
        'solved': '\033[41m',
    }
    RESET = '\033[0m'
    for row in grid:
        print(''.join(f"{CELL_COLORS[cell]} {RESET}" for cell in row
                      if cell in CELL_COLORS))


if __name__ == "__main__":
    render(create_grid())
