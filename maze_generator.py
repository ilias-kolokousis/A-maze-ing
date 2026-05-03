#!/usr/bin/env python3

from pydantic import Field, BaseModel, model_validator
import os
from a_maze_ing import handle_errors
from src.maze_class import Maze
from src.prims import generate_prim
from src.hunt_n_kill import generate_hunt_n_kill


class MazeGenerator(BaseModel):
    """MazeGenerator object that generates a maze
    with the MazeGenerator.generate function

    Raises:
        ValueError: when something is not correctly
            put in
    """
    seed: int | None = Field(default=None)
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool = Field(default=True)

    @model_validator(mode='after')
    def validate_gen(self) -> 'MazeGenerator':
        """Validate the data to check for errors"""
        if (self.width * 2 * 2 > os.get_terminal_size().columns
           or self.height * 2 > os.get_terminal_size().lines):
            raise ValueError("Error: Height and width is too big."
                             "It won't render correctly."
                             "\nPlease put smaller values in "
                             "or resize your terminal.")
        if not (0 <= self.entry[0] < self.width
                and 0 <= self.exit[0] < self.width
                and 0 <= self.entry[1] < self.height
                and 0 <= self.exit[1] < self.height):
            raise ValueError("Error: Values inside entry and exit must be "
                             f"between 0 and {self.width}"
                             " for the first value "
                             "of entry and exit and"
                             f"between 0 and {self.height} "
                             "for the second value of entry and exit"
                             f"\nGot '{self.entry[0]}' and "
                             f"'{self.exit[1]}'")
        return self

    def generate(self) -> None:
        """Checks for errors, and when none are found, decides on the
     algorithm to use. When the perfect key is true, it uses
     prims algorithm. Otherwise it uses hunt-n-kill algorithm
        """
        config: dict[str, str] = {
            'seed': str(self.seed),
            'width': str(self.width),
            'height': str(self.height),
            'entry': str(self.entry).strip('(').strip(')'),
            'exit': str(self.exit).strip('(').strip(')'),
            'output_file': str(self.output_file),
            'perfect': str(self.perfect)
        }

        if not handle_errors(config):
            return

        maze: Maze = Maze(config)
        if self.perfect:
            generate_prim(maze)
        else:
            generate_hunt_n_kill(maze)


if __name__ == "__main__":
    print(MazeGenerator)
