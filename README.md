_This project has been created as part of the 42 curriculum by <ikolokou>, <lvan-hem>_

# A-Maze-ing

## Description
A Python-based maze generator that produces mazes from a simple configuration file, encoding the result in a hexadecimal wall representation format.

### Overview
The program takes a configuration file as input and generates a maze according to the specified parameters. It supports both perfect and imperfect mazes. Any maze can be reproduced exactly by providing the same seed value.
Each cell in the output is encoded as a single hexadecimal digit, where each bit represents the presence or absence of a wall on a given side (North, East, South, West). The output file contains the full grid, the entry and exit coordinates, and the shortest path between them expressed as a cardinal direction sequence.
All generated mazes embed a "42" pattern formed by fully enclosed cells — omitted with a warning if the maze dimensions are too small to accommodate it.

### Constraints
- No open area may exceed 2 cells in width or height — large rooms are not permitted
- Shared walls between adjacent cells must be consistent across both cells
- Entry and exit must be distinct and lie within the maze bounds
- The outer border is fully walled.
- In perfect mode, the maze is guaranteed to contain exactly one path from entry to exit


## Instructions
The program can be run, by running the command _make run_. This will utilise the Makefile, and launch the program.

_make run_ is dependent on _make install_. This command will run automatically when you run _make run_. 

If you want to clean up the source directory of the program, run _make clean_.

A list of all the make commands:

- _make install_
 Installs all requirements that are present in the requirements.txt file. It also installs venv (Virtual Environment)
 __Requirements:__
 - annotated-types==0.7.0
 - flake8==7.3.0
 - librt==0.9.0
 - mccabe==0.7.0
 - mypy==1.20.2
 - mypy_extensions==1.1.0
 - pathspec==1.1.1
 - pycodestyle==2.14.0
 - pydantic==2.11.0
 - pydantic-settings==2.14.0
 - pydantic_core==2.33.0
 - pyflakes==3.4.0
 - python-dotenv==1.2.2
 - typing-inspection==0.4.2
 - typing_extensions==4.15.0

- _make run_
 Checks if all the requirements are installed, then launches the program when they are. It runs it from a virtual environment installed in the root.

- _make debug_
 Runs programm with Python debugger (pdb)

- _make lint_
 Checks for flake8 and mypy errors in the source code.

- _make lint-strict_
 Checks for flake8 and mypy errors, with the flag --strict for mypy. (Optional)

- _make clean_
 Deletes all files created during runtime, as well as pychaches.


## Resources

### References
- Python Makefile: https://earthly.dev/blog/python-makefile/

- Prims algorithm: https://www.youtube.com/watch?v=20QfaLQPLqQ

- Maze generation algorithms: https://www.youtube.com/watch?v=ioUl1M77hww

- Prims and Kruskals algorithm: https://www.geeksforgeeks.org/dsa/difference-between-prims-and-kruskals-algorithm-for-mst/

### AI Usage
Claude Sonnet 4.6 has been used to discuss different forms of implementation, and to answer questions about Makefile and Python syntaxes. It also helped cleaning up mypy errors. 


## Config file
seed=0
width=20
height=20
entry=0,0
exit=19,19
output_file=maze.txt
perfect=true

This default config file gives entry and exit, as well as the size and if its a perfect maze. 

A randomly generated maze will have a minimum size of 4x4, and a maximum size of 40x40.

7x9 is the minimum size for a maze to be generated with the 42 cells in the middle closed off.

All parameters are randomised within certain limits e.g. entry cannot be same as exit and both will never be inside the 42 cells. Height cannot be more than width.

The seed is generated first, and used to set parameters as well as generate the maze, so that the exact maze is reproducable with the seed.


## Algorithms
We decided to implement two algorithms: Prim's and Hunt-N-Kill.

To generate a perfect maze, we utilised Prim's algorithm. We made this decision because Prim's algorithm always generates a perfect maze.

To generate an imperfect maze, we utilised Hunt-N-Kill algorithm, since its easily modifyable to create loops, thus creating an imperfect maze.


## Reusability

This project can be also isntalled with `pip install`. Steps:

1. 
```bash
pip install a-maze-ing-generator-il-lu
```
2. Import it in your python project:
```python 
from mazegen_il_lu import MazeGenerator
```
3. Define a MazeGenerator class with the following attributes:
	- seed (int), 
	- width (int), 
	- height(int), 
	- entry(tuple[int, int]), 
	- exit(tuple[int, int]), 
	- output_file(str), 
	- perfect(default False)

4. Use the generate method to generate a maze.
```python
MazeGenerator(...).generate()
```  

## Project Managment
The division of roles went very natural. We wrote down a list of tasks, and choose some tasks to do.
We both wrote one algorithm, and the other parts of the project were divided.

The project went according to plan, without sudden roadblocks. We came together to discuss code, and kept in contact.

What went well was the steady progress. Our project was under development the whole time.

What could've been improved was clearer meeting times. We did not really schedule specific dates/times always to discuss our code.

Our tools used are:
Slack - to communicate
Github - to push code, and checkout the other person's code

## Advanced features
Our maze generation utilises two different algorithms: Prim's and Hunt-N-Kill.

Our maze generation is also visualised in real-time. 
