import re
import math

def parse(lines):
    paths = {}
    for line in lines:
        mtch = re.match(r'(.*) = \((.*), (.*)\)', line)
        paths[mtch[1]] = (mtch[2], mtch[3])
    return paths

def search(field, start, end_cond):
    paths, steps = field
    step = 0
    state = start
    while not end_cond(state):
        i = step % len(steps)
        state = paths[state][steps[i]]
        step += 1
    return step


def run(file):
    lines = file.split('\n')
    steps = [0 if c == 'L' else 1 for c in lines[0]]
    paths = parse(lines[2:])
    field = (paths, steps)

    # Part 1
    print(search(field, 'AAA', lambda s: s == 'ZZZ'))
    
    # Part 2
    states = [x for x in paths if x[-1] == 'A']
    lcm = 1
    for start in states:
        length = search(field, start, lambda s: s[-1] == 'Z')
        lcm = lcm * length // math.gcd(lcm, length)
        
    print(lcm)

