import re

# Part 1
def parse_rule(line):
    name, *rules = re.split(r'[{,}]', line)
    parsed = []
    for rule in rules[:-1]:
        var, op, limit, dst = re.match(r'(?:(\w+)([<>])(\d+):)?(\w+)', rule).groups()
        limit = int(limit) if limit else None
        if op == '<':
            limit -= 1 # Use <= instead of < for easier range splitting
        parsed.append({"var":var, "op":op, "limit":limit, "dst":dst})
    return name, parsed

def parse_part(line):
    assigns = [x.split('=') for x in line[1:-1].split(',')]
    return {a[0]: int(a[1]) for a in assigns}

def matches(rule, part):
    if not rule["op"]:
        return True

    val = part[rule["var"]]
    if rule["op"] == ">":
        return val > rule["limit"]
    return val <= rule["limit"]

def end_state(rule_dict, part):
    state = "in"
    while state in rule_dict:
        rules = rule_dict[state]
        for rule in rules:
            if matches(rule, part):
                state = rule["dst"]
                break
    return state

# Part 2
# The state is a four-tuple (per-category) of two-tuples (start and end of a range)
def split(ranges, rule):
    """Divides the tuple of ranges into one that matches the rule and one that doesn't"""
    if not rule["op"]:
        return ranges, None 

    # Get the item of the tuple that corresponds to the checked range
    split_index = "xmas".index(rule["var"])
    split_range = ranges[split_index]

    op, limit = rule["op"], rule["limit"]
    start, end = split_range
    # Split the one tuple based on the rule
    if start > limit:
        left, right = None, changed
    elif end <= limit:
        left, right = changed, None
    else:
        left, right = (start, limit), (limit + 1, end) 

    # Reconstruct the resulting tuples based on the split
    ranges = list(ranges)
    ranges[split_index] = left
    matched = tuple(ranges) if left else None
    ranges[split_index] = right
    unmatched = tuple(ranges) if right else None

    return (matched, unmatched) if op == '<' else (unmatched, matched)

def dfs(rule_dict):
    # Ranges are inclusive on both sides
    start = ("in", tuple((1, 4000) for _ in "xmas"))
    found = set()
    stack = [start]
    while stack:
        state, ranges = stack.pop()
        rules = rule_dict.get(state, [])
        for rule in rules:
            matched, ranges = split(ranges, rule)
            if not matched:
                continue
            key = (rule["dst"], matched)
            if key not in found:
                found.add(key)
                stack.append(key)
            if not ranges:
                break
    return found

def combinations(ranges):
    total = 1
    for r in ranges:
        start, end = r
        total *= end - start + 1
    return total

def run(blocks, timer):
    rules, parts = blocks
    rules = {n:p for n, p in map(parse_rule, rules)}
    parts = list(map(parse_part, parts))
    states = [end_state(rules, p) for p in parts]
    print(sum(sum(p.values()) for i, p in enumerate(parts) if states[i] == 'A'))

    timer.tick()

    found = dfs(rules)
    accepted = [s[1] for s in found if s[0] == 'A']
    print(sum(combinations(c) for c in accepted))
 
