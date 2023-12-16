def dfs(start, get_next):
    visited = {start}
    stack = [start]
    while stack:
        current = stack.pop()
        for neighbor in get_next(current):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append(neighbor)
    return visited

class Grid:
    out_direction = {
        '.': {'up': ('up',), 'down': ('down',), 'left': ('left',), 'right': ('right',)},
        '-': {'up': ('left', 'right'), 'down': ('left', 'right'), 'left': ('left',), 'right': ('right',)},
        '|': {'up': ('up',), 'down': ('down',), 'left': ('up', 'down'), 'right': ('up', 'down')},
        '\\': {'up': ('left',), 'down': ('right',), 'left': ('up',), 'right': ('down',)},
        '/': {'up': ('right',), 'down': ('left',), 'left': ('down',), 'right': ('up',)}
    }
    shift = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}
    opposite = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    
    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def get_next(self, move):
        x, y, in_dir = move
        for out in Grid.out_direction[self.grid[x][y]][in_dir]:
            dx, dy = Grid.shift[out]
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.height and 0 <= ny < self.width:
                yield nx, ny, out

def count_places(visited):
    return len(set((v[0], v[1]) for v in visited))

def run(lines):
    grid = Grid(lines)
    visited = dfs((0, 0, 'right'), grid.get_next)
    print(count_places(visited))

    opposite_starts = set() # entry points with starting directions reversed
    for i in range(grid.height):
        opposite_starts.add((i, 0, 'left'))
        opposite_starts.add((i, grid.width-1, 'right'))
    for i in range(grid.width):
        opposite_starts.add((0, i, 'up'))
        opposite_starts.add((grid.height-1, i, 'down'))

    most = 0
    while opposite_starts:
        x, y, d = opposite_starts.pop()
        visited = dfs((x, y, Grid.opposite[d]), grid.get_next)
        most = max(most, count_places(visited))
        opposite_starts.difference_update(visited) # this is why the start directions are reversed

    print(most)
