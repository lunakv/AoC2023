def parse(block):
    return [list(line) for line in block.split('\n')]

def stringify(grid):
    return '\n'.join(''.join(row) for row in grid)

def tilt_up(grid):
    filled_row = [-1] * len(grid[0])
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            symbol = grid[i][j]
            if symbol == '#':
                filled_row[j] = i
            if symbol == 'O':
                filled_row[j] += 1
                if i != filled_row[j]:
                    grid[filled_row[j]][j] = 'O'
                    grid[i][j] = '.'
    return grid

def rotate_clockwise(grid):
    # clockwise rotation is a transposition followed by a horizontal flip
    return [[grid[len(grid)-1-j][i] for j in range(len(grid))] for i in range(len(grid[0]))]

def cycle(grid):
    for _ in range(4):
        grid = tilt_up(grid)
        grid = rotate_clockwise(grid)
    return grid

def repeated_cycle(grid, cycle_count):
    grid_to_cycle = {stringify(grid): 0}
    cycle_to_grid= [stringify(grid)]

    for i in range(cycle_count):
        new_grid = cycle(grid)
        key = stringify(new_grid)

        if key in grid_to_cycle:
            start = grid_to_cycle[key]
            offset = (cycle_count - start) % (i+1 - start)
            return parse(cycle_to_grid[start + offset])
        else:
            grid_to_cycle[key] = i+1
            cycle_to_grid.append(key)
            grid = new_grid
    return grid

def get_score(grid):
    total = 0
    for i, row in enumerate(grid):
        total += (len(grid)-i) * sum(c == 'O' for c in row)
    return total

def run(file, timer):
    grid = parse(file)
    print(get_score(tilt_up(grid)))

    timer.tick()

    grid = parse(file)
    print(get_score(repeated_cycle(grid, 1_000_000_000)))
