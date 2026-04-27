#!/usr/bin/env python3

from src.maze_class import Maze
from hunt_n_kill import create_maze
from time import sleep


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


def get_input(maze: Maze, solution_rendered: bool = False) -> None:
    """Ask user for input when maze has been generated.

    Args:
        maze (Maze): maze object
        solution_rendered (bool): checks if solution path is showing"""
    print("=== A-Maze-ing ==="
          "\n\t1. Regenerate a new maze"
          "\n\t2. Show/Hide path from entry to exit"
          "\n\t3. Choose new colors"
          "\n\t4. Quit")
    choice: str = input("Choice? (1-4): ")
    if choice == '1':
        print("\033[2J\033[H", end="", flush=True)
        maze.grid_init()
        if maze.perfect:
            print("Prim's algo")
        else:
            create_maze(maze)
    elif choice == '2':
        viz: Viz = Viz(maze.output_file, maze.coords_42)
        if solution_rendered:
            print("\033[2J\033[H", end="", flush=True)
            viz.render(viz.output)
            get_input(maze)
        else:
            print("\033[2J\033[H", end="", flush=True)
            viz.render(viz.output_w_solution)
            get_input(maze, True)
    elif choice == '3':
        viz: Viz = Viz(maze.output_file, maze.coords_42)
        print("==========")
        print("Choose the # corresponding to the desired color:"
              "\n\t1. Black"
              "\n\t2. Red"
              "\n\t3. Green"
              "\n\t4. Yellow"
              "\n\t5. Blue"
              "\n\t6. Purple"
              "\n\t7. Cyan"
              "\n\t8. White")
        walls: str = input('Walls (choice: 1-8): ')
        path: str = input('Path (choice: 1-8): ')
        start: str = input('Start (choice: 1-8): ')
        end: str = input('End (choice: 1-8): ')
        fourty_two: str = input('42 (choice: 1-8): ')
        solution: str = input('Solution (choice: 1-8): ')
        answers: list[str] = [walls, path, start, end, fourty_two, solution]
        for answer in answers:
            if int(answer.strip('.')) not in set(range(1, 9)):
                print("\033[2J\033[H", end="", flush=True)
                if solution_rendered:
                    viz.render(viz.output_w_solution)
                    print("""
        \033[1;31mPlease put a number in from 1 to 8 only in colors\033[0m
                    """)
                    get_input(maze, True)
                    return
                else:
                    viz.render(viz.output)
                    print("""
        \033[1;31mPlease put a number in from 1 to 8 only in colors\033[0m
                    """)
                    get_input(maze)
                    return

        answer_dict: dict[str, str] = {
            '1': 'Black',
            '2': 'Red',
            '3': 'Green',
            '4': 'Yellow',
            '5': 'Blue',
            '6': 'Purple',
            '7': 'Cyan',
            '8': 'White'
        }

        viz.CELL_COLORS['wall'] = viz.COLORS[answer_dict[walls.strip('.')]]
        viz.CELL_COLORS['path'] = viz.COLORS[answer_dict[path.strip('.')]]
        viz.CELL_COLORS['start'] = viz.COLORS[answer_dict[start.strip('.')]]
        viz.CELL_COLORS['end'] = viz.COLORS[answer_dict[end.strip('.')]]
        viz.CELL_COLORS['coord'] = viz.COLORS[
            answer_dict[fourty_two.strip('.')]]
        viz.CELL_COLORS['solved'] = viz.COLORS[
            answer_dict[solution.strip('.')]]

        print("\033[2J\033[H", end="", flush=True)
        if solution_rendered:
            viz.render(viz.output_w_solution)
            get_input(maze, True)
        else:
            viz.render(viz.output)
            get_input(maze)
    elif choice == '4':
        return
    else:
        print("\033[2J\033[H", end="", flush=True)
        viz: Viz = Viz(maze.output_file, maze.coords_42)
        if solution_rendered:
            viz.render(viz.output_w_solution)
            print(
                "\033[1;31mPlease put a number in from 1 to 4 only\033[0m"
                )
            get_input(maze, True)
        else:
            viz.render(viz.output)
            print(
                "\033[1;31mPlease put a number in from 1 to 4 only\033[0m"
                )
            get_input(maze)


def create_output_file(maze: Maze) -> None:
    """Create an output file for the maze in hex format.

    Args:
        maze (Maze): Maze class that has all relevant attributes
    """
    grid: list[list[str]] = [row[:] for row in maze.grid]
    entry: str = f'{maze.entry[0]},{maze.entry[1]}'
    exit: str = f'{maze.exit[0]},{maze.exit[1]}'

    for row in range(maze.height):
        for cell in range(maze.width):
            grid[row][cell] = str(hex(maze.grid[row][cell]))[2:].upper()

    output: str = ''
    for row in grid:
        output += ''.join(row) + '\n'
    output += f'\n{entry}\n{exit}\n'
    with open(maze.output_file, 'w') as f:
        f.write(output)


def print_state(maze: Maze) -> None:
    """Print current state of the maze

    Args:
        maze (Maze): Maze class with the relevant attributes
    """
    create_output_file(maze)
    sleep(0.05)
    print("\033[H", end="", flush=True)
    viz: Viz = Viz(maze.output_file, maze.coords_42)
    viz.render(viz.output)
    print("\033[J")


if __name__ == "__main__":
    print()
