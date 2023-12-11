def expand(field, factor):
    nonempty_cols = set()
    nonempty_rows = set()
    for i, line in enumerate(field):
        galaxies = [j for j, c in enumerate(line) if c != '.']
        if galaxies:
            nonempty_rows.add(i)
        nonempty_cols.update(galaxies)

    row_values = [1 if i in nonempty_rows else factor for i in range(len(field))]
    col_values = [1 if i in nonempty_cols else factor for i in range(len(field[0]))]
    return row_values, col_values

def find_galaxies(field):
    res = []
    for i, line in enumerate(field):
        for j, c in enumerate(line):
            if c == '#':
                res.append((i, j))
    return res

def distance(a, b, values):
    row_vals, col_vals = values
    start, end = min(a[0], b[0]), max(a[0], b[0])
    row_distance = sum(row_vals[start+1:end+1])
    start, end = min(a[1], b[1]), max(a[1], b[1])
    col_distance = sum(col_vals[start+1:end+1])
    return row_distance + col_distance

def run(lines):
    galaxies = find_galaxies(lines)
    values_1 = expand(lines, 2)
    values_2 = expand(lines, 1000000)
    total_1 = 0
    total_2 = 0
    for i, a in enumerate(galaxies):
        for b in galaxies[i+1:]:
            total_1 += distance(a, b, values_1)
            total_2 += distance(a, b, values_2)

    print(total_1)
    print(total_2)

