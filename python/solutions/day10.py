directions = ['up', 'right', 'down', 'left']
def rotate_clockwise(direction):
    return directions[(directions.index(direction) + 1) % 4]

def rotate_counterclockwise(direction):
    return directions[(directions.index(direction) + 3) % 4]

def get_out_direction(char, in_direction):
    if char == '|' or char == '-':
        return in_direction
    if char == 'F':
        return 'right' if in_direction == 'up' else 'down'
    if char == 'L':
        return 'right' if in_direction == 'down' else 'up'
    if char == 'J':
        return 'left' if in_direction == 'down' else 'up'
    if char == '7':
        return 'left' if in_direction == 'up' else 'down'

def move(x, y, direction):
    if direction == 'up':
        return x-1, y
    if direction == 'down':
        return x+1, y
    if direction == 'left':
        return x, y-1
    return x, y+1
    
def connected_directions(x, y, lines):
    """Determine the directions which have tiles connected to this one"""
    directions = []
    if x > 0 and lines[x-1][y] in ['|', 'F', '7']:
        directions.append('up')
    if x < len(lines) - 1 and lines[x+1][y] in ['|', 'L', 'J']:
        directions.append('down')
    if y > 0 and lines[x][y-1] in ['-', 'L', 'F']:
        directions.append('left')
    if y < len(lines[x]) - 1 and lines[x][y+1] in ['-', 'J', '7']:
        directions.append('right')
    return directions

def get_starting_direction(directions):
    """A consistent starting direction for the walk"""
    a, b = directions
    return a if b == rotate_clockwise(a) else b

def find_start(lines):
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == 'S':
                return (i, j)

def search_nonloop_tiles(start, field, loop):
    """
    Returns all non-loop tiles that are reachable from the starting position
    """
    visited = set()
    stack = [start]
    while stack:
        x, y = stack.pop()
        visited.add((x, y))
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < len(field) and 0 <= ny < len(field[nx]) and (nx, ny) not in loop and (nx, ny) not in visited:
                stack.append((nx, ny))

    return visited

def walk_loop(sx, sy, field, callback):
    """
    Walk the loop, calling the callback on each non-start tile visited

    Returns the set of all positions visited during the walk
    """
    loop = set()
    loop.add((sx, sy))
    in_direction = get_starting_direction(connected_directions(sx, sy, field))
    x, y = move(sx, sy, in_direction)
    while (x, y) != (sx, sy):
        loop.add((x, y))
        out_direction = get_out_direction(field[x][y], in_direction)
        callback(x, y, in_direction, out_direction)
        x, y = move(x, y, out_direction)
        in_direction = out_direction 

    return loop


def run(lines, timer):
    sx, sy = find_start(lines)
    # Determine the overall direction of the loop
    clockwise_turns = 0
    def count_turns(x, y, in_direction, out_direction):
        nonlocal clockwise_turns
        if out_direction == rotate_clockwise(in_direction):
            clockwise_turns += 1
        elif out_direction == rotate_counterclockwise(in_direction):
            clockwise_turns -= 1

    loop = walk_loop(sx, sy, lines, count_turns) 
    # Part 1 
    print(len(loop) // 2)

    timer.tick()
    # Mark tiles that are on the inside of any loop segment
    inside_turn = rotate_clockwise if clockwise_turns > 0 else rotate_counterclockwise
    marked_inside = set()
    def mark_inside(x, y, in_direction, out_direction):
        nonlocal marked_inside
        for segment in (in_direction, out_direction):
            inside_x, inside_y = move(x, y, inside_turn(segment))
            if (inside_x, inside_y) not in loop:
                marked_inside.add((inside_x, inside_y))
                
    walk_loop(sx, sy, lines, mark_inside)
    
    # Count all tiles that are connected to some marked tile 
    inside_count = 0
    while marked_inside:
        tiles = search_nonloop_tiles(marked_inside.pop(), lines, loop)
        inside_count += len(tiles)
        marked_inside.difference_update(tiles)

    # Part 2
    print(inside_count)

