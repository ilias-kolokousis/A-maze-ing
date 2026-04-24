#!/usr/bin/env python3

class Viz():
    COLORS: dict[str, str] = {'Black': '\033[40m',
                              'Red': '\033[41m',
                              'Green': '\033[42m',
                              'Yellow': '\033[43m',
                              'Blue': '\033[44m',
                              'Purple': '\033[45m',
                              'Cyan': '\033[46m',
                              'White': '\033[47m'}
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
    CELL_COLORS = {
            'wall':   COLORS['White'],
            'path':   COLORS['Black'],
            'start':  COLORS['Purple'],
            'end':    COLORS['Blue'],
            'solved': COLORS['Red'],
            'coord':  COLORS['Cyan']
        }

    def __init__(self, path: str, coords_42: list[tuple[int, int]]) -> None:
        self.output_path: str = path
        with open(self.output_path, 'r') as f:
            self.maze: str = f.read()

        self.width: int = len(self.maze.split('\n')[0])
        self.height: int = len(self.maze.split('\n')[:-3]) - 1
        self.path: str = self.maze.split('\n')[-1]
        self.coords_42: list[tuple[int, int]] = coords_42

    @property
    def start(self) -> tuple[int, int]:
        start_raw: tuple = tuple(
            int(i)
            for i in self.maze.split('\n')[-3].split(',')
            )
        return (int(start_raw[0]) * 2 + 1, int(start_raw[1]) * 2 + 1)

    @property
    def end(self) -> tuple[int, int]:
        end_raw: tuple = tuple(
            int(i)
            for i in self.maze.split('\n')[-2].split(',')
            )
        return (int(end_raw[0]) * 2 + 1, int(end_raw[1]) * 2 + 1)

    def create_paths_in_rows(self, output: list[list[str]],
                             width: int) -> list[list[str]]:
        for row in range(len(output)):
            if row % 2 == 0:
                visual_width = width * 2
                output[row] = ['wall'] * (visual_width + 1)
            else:
                for cell in range(len(output[row])):
                    if output[row][cell] not in self.HEX_TO_BIN:
                        continue
                    encoding: list = list(self.HEX_TO_BIN[output[row][cell]])
                    if encoding[2] == '0':
                        output[row][cell + 1] = 'path'
        return output

    def create_paths_in_columns(self,
                                output: list[list[str]]) -> list[list[str]]:
        for row in range(len(output)):
            for cell in range(len(output[row])):
                if output[row][cell] not in self.HEX_TO_BIN:
                    continue
                encoding: list = list(self.HEX_TO_BIN[output[row][cell]])
                if encoding[1] == '0':
                    output[row + 1][cell] = 'path'
                if output[row][cell] != 'wall':
                    output[row][cell] = 'path'
        return output

    def create_walls_and_paths(self) -> list[list[str]]:
        maze_lst: list = [interchange_list_element(list(row), 'wall',
                                                   self.width)
                          for row in self.maze.split('\n')[:-4]]
        output: list = interchange_list_element(maze_lst, ['wall'],
                                                self.height)
        output = self.create_paths_in_rows(output, self.width)
        output = self.create_paths_in_columns(output)
        return output

    @property
    def output(self) -> list[list[str]]:
        output: list[list[str]] = self.create_walls_and_paths()
        for coord in self.coords_42:
            output[coord[1] * 2 + 1][coord[0] * 2 + 1] = 'coord'
        output[self.start[1]][self.start[0]] = 'start'
        output[self.end[1]][self.end[0]] = 'end'
        return output

    def create_solution_path(self) -> list[list[str]]:
        grid: list[list[str]] = [row[:] for row in self.output]
        current_cell: tuple = self.start[:]
        for direction in self.path:
            if direction == 'N':
                current_cell = current_cell[0], current_cell[1] - 2
                grid[current_cell[1] + 1][current_cell[0]] = 'solved'
            elif direction == 'S':
                current_cell = current_cell[0], current_cell[1] + 2
                grid[current_cell[1] - 1][current_cell[0]] = 'solved'
            elif direction == 'E':
                current_cell = current_cell[0] + 2, current_cell[1]
                grid[current_cell[1]][current_cell[0] - 1] = 'solved'
            elif direction == 'W':
                current_cell = current_cell[0] - 2, current_cell[1]
                grid[current_cell[1]][current_cell[0] + 1] = 'solved'
            grid[current_cell[1]][current_cell[0]] = 'solved'
        grid[self.start[1]][self.start[0]] = 'start'
        grid[self.end[1]][self.end[0]] = 'end'
        return grid

    @property
    def output_w_solution(self) -> list[list[str]]:
        return self.create_solution_path()

    def render(self, output: list[list[str]]) -> None:
        RESET = '\033[0m'
        for row in output:
            print(''.join(f"{self.CELL_COLORS[cell]}  {RESET}" for cell in row
                          if cell in self.CELL_COLORS))


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


if __name__ == "__main__":
    print()
