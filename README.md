# A-Maze-ing

## Algorithms used for maze generation:

### **Prim's Algorithm:**
- Subgraph connecting all vertices
- No cycles
- Always looks for minimum cost
- The MST of N vertices has N - 1 edges, an extra edge will cause a cycle

**How it works:**
- Start from any vertex
- Select the edge with the smallest weight at each step
- Repeat the second step until all vertices are connected (N - 1 edges)

**Required data structures:**
- Visited Set: []
    Keeps track of visited vertices
- Min Heap
    A priority queue, to efficiently select the edge with the smalles weight at each step
- MST List
    A list to store the edges to make up the final minimum spanning tree

**How the algorithm works:**
- Loop through all the edges, and for every vertex, store a list of tupils 
    containing the edge's weight and its neighbouring vertex
- Create a set called nodes, to keep track of all the unique vertices in the graph

- *Initialize four variables:*
    - visited = set()   : A set to track visited vertices
    - mst = []          : A list to store the edges included in the minimum spanning tree
    - total_weight = 0  : A variable to accumulate the total weight of the spanning tree
    - min_heap = []     : A priority queue to select the next edge with the smallest weight

- *Choose any starting point:*
    start = edges [0][0]
- *Mark starting point as visited:*
    visited.add(start)
- *Add all edges eminating from this starting vertex to min_heap:*
    for weight, neighbour in graph[start]:
        heapq.heappush(min_heap, (weight, start, neighbour))

- The main loop starts running
    and the loop continues as long as the min-heap isn't empty
        and mst of N vertices is smaller than N - 1

- *Each iteration:*
    - Pop the edge with the smallest weight from the priority queue
    - If vertex hasn't been visited, mark is as visited
        else, continue to the next vertex in min_heap
    - Add the edge to the spanning tree,
        and update the total weight
    - Add all new edges to the priority queue
        provided they connect to unvisited vertices

**When N - 1 edges have been reached, the function returns the list with edges in the tree,**
    **along with the total weight**

```python
import heapq
from collcections import defaultdict

def prim(edges):
    graph = defaultdict(list)
    nodes = set()
    for u, v, w in edges:
        graph[u].append((w, v))
        graph[v].append((w, u))
        nodes.update([u, v])
    
    visited = set()
    mst = []
    total_weight = 0
    min_heap = []

    start = edges[0][0]
    visited.add(start)
    for weight, neighbour in graph[start]:
        heapq.heappush(min_heap, (weight, start, neighbour))
    
    while min_heap and len(mst) < len(nodes) - 1:
        weight, u, v = heapq.heappop(min_heap)
        if v not in visited:
            visited.add(v)
            mst.append((u, v, weight))
            total_weight += weight
            for next_weight, neighbour in graph[v]:
                if neighbour not in visited:
                    heapq.heappush(min_heap, (next_weight, v, neighbour))

    return mst, total_weight
```

### **Kruskal's Algorithm:**
- Similar to Prim's algorithm
- A greedy algorithm, that in each step adds to the forest 
    the lowest weight edge that will not form a cycle
- Key steps are sorting, and the use of a disjoint-set data structure to detect cycles

**How the algorithm works:**
- Create a forest (a set of trees) initially consisting of a 
    seperate single-vertex tree for each vertex in the nput graph
- Sort the graph edges by weight
- Loop through the edges of the graph, in ascending order by their weight
    For each edge:
    - Test wether adding the edge to the current forest would create a cycle
    - If not, add the edge to the forest, combining two trees into as single tree

### **Kruskal vs Prim**
|Feature|Prim's Algorithm|Kruskal's Algorithm|
|-------|----------------|-------------------|
|'Approach'|Vertex-based, grows the MST one vertex at a time|Edge based, adds edges in increasing order of weight|
|'Data structure'|Priority queue (min-heap)|Union-Find data structur|
|'Graph representation'|Adjacency matrix or adjacency list|Edge list|
|'Initialization'|Starts from an arbitrary vertex|Starts with all vertices as separate trees (forest)|
|'Edge selection'|Chooses the minimum weight edge from the connected vertices|Chooses the minimum weight edge from all edges|
|'Cycle management'|Not explicitly managed; grows connected component|Uses Union-Find to avoid cycles|
|'Complexity'|O(V^2) for adjacency matrix, O((E + V) log V) with a priority queue|O(E log E) or O(E log V), due to edge sorting|
|'Suitable for'|Dense graphs|Sparse graphs|
|'Implementation complexity'|Relatively simpler in dense graphs|More complex due to cycle management|
|'Parallelism'|Difficult to parallelize|Easier to parallelize edge sorting and union operations|
|'Memory usage'|More memory for priority queue|Less memory of edges can be sorted externally|
|'Example use cases'|Network design, clustering with dense connections|Road networks, telecommunications with sparse connections|
|'Starting point'|Requires a starting vertex|No specific starting point, operates on global edges|
|'Optimal for'|Dense graphs where adjacency list is used|Sparse graphs where edge list is efficient|

### **Backtracking Algorithm**
**Backtracking algorithms** are strategies that help explore different options to find the solution.
- Work by tring out different paths and if one doen't work, then backtrack and try another until the right one is found. 
    Its like solving a puzzle by testing different pieces until they fit together perfectly
- Useful for problems where you must generate all valid combinations, permutations, or subsets under constraints

*How does a backtracking algorithm work?*
A backtracking algorithm works by recursively exploring all pssible solutions to a problem. It starts by choosing an initial solution, and then it explores all possible extensions of that solution. If an extension leads to a solution, the algorithm returns that solution. If an extension does not lead to a solution, the algorithm backtracks to the previous solution and tries a different extension.

**A general outline of how a backtracking algorithm works:**
1. Choose an initial solution
2. Explore all possible extensions of the current solution
3. If an extension leads to a solution, return that solution
4. If an extension doesn't lead to a solution, backtrack to the previous solution and try a different extension.
5. Repeat steps 2-4 until all possible solutions have been explored.

### **Depth First Search (DFS)**
Also known as the backtracking maze.

*How it is generated*
1. Start with a grid where every cell is surrounded by walls
2.  - Select a random starting cell
    - Mark it as visited
    - Look at neighbouring cells
3. Select a random unvisited neighbour
4.  - Go to the selected cell
    - Mark it as visited
    - Remove the wall between current and previous cell
5. If there is no unvisited cell:
    1. Backtrack to previous cell
    2. Repeat until an unvisited neighbour cell is found
6. Repeat step 3-5 until all cells are visited

### **Hunt and Kill Algorithm**

*How it is generated*
1. Start with a grid where every cell is surrounded by walls
2.  - Select a random starting cell
    - Mark it as visited
    - Look at neighbouring cells
3. Select a random unvisited neighbour
4.  - Go to the selected cell
    - Mark it as visited
    - Remove the wall between current and previous cell
5. Repeat steps 3 and 4, until there is no unvisited neighbour cell
6. If there is no unvisited neighbour cell:
    1. Iterate through the visited cell
    2. Stop when found a cell with an unvisited neighbour
    3. Select this cell, and continue starting at step 3
7. Repeat until all cells are visited

### **Prim's Algorithm to generate a Maze**

*How it is generated*
1. Start with a grid where every cell is surrounded by walls
2. Select random starting cell
3. Add it walls to the list
4. Select a random wall, and if it separates a new cell from a visited one, remove it.
5. Repeat until all cells are visited

- Prim's Algorithm is ideal to generate a perfect maze
- It ensures all cells are connected, but only one path from start to finish exists

## Seeded maze generation
A seed ensures the same maze is generated everytime!

### random.seed() method
The random.seed() method in Python is used to initialize the random number generator so that it produces the same squence of random numbers every time a program is run. By setting a fixed seed value, randomness becomes reproducible, which is essential for debugging, testing and scientific experiments.

- Ensures consistent results across multiple executions
- Helps in debugging and verifying program output
- Supports reproducible experiments in machine learning and simulations
- Useful for controlled randomness in game development and testing

*Example:*
```Python
import random

for i in range(2):
    print(random.randint(1, 1000))

for i in range(2):
    random.seed(0)
    print(random.randint(1, 1000))
```

**Output:**

*Without seed:*
> - 21
> - 537

*With seed:*
> - 865
> - 865

### Syntax
> random.seed(a=None, version=2)

**Parameters:**
- **a (optional):** it's the seed value (int, float, str, bytes or bytearray). If None, the system time is used
- **version (optional):** default value is 2, using a more advanced seeding algorithm. version=1 uses an older method

**Return type:**
random.seed() method does not return any value

## Configuration file
A configuration file is a plain text file used to store application settings and parameters in a readable format.

- Settings are usually written as key-value pairs
- The INI (initialization) format is popular because it is simple and easy to read
- Python provides the configparser module to work with INI files
- The module allows reading from and writing to configuration files efficiently

### Creating a configuration file in Python
```Python
import configparser

def create_config():
    config = configparser.ConfigParser()
    config["DEFAULT"] = {
        "SEED": None,
        "WIDTH": 20,
        "HEIGHT": 20,
        "ENTRY": (0, 0),
        "EXIT": (19, 19),
        "OUTPUT_FILE": "maze.txt",
        "PERFECT": True
    }
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

if __name__ == "__main__":
    create_config()
```

## Makefile

**Good source:** https://earthly.dev/blog/python-makefile/

