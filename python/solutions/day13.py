def find_mirror_line(field, expected_difference):
    for i in range(1, len(field)):
        difference = 0
        for j in range(min(i, len(field)-i)):
            top_line = field[i-j-1]
            bottom_line = field[i+j]
            difference += sum(top_line[c] != bottom_line[c] for c in range(len(top_line)))
        if difference == expected_difference:
            return i

    return 0

def get_block_score(block, expected_difference):
    mirror = find_mirror_line(block, expected_difference)
    if mirror:
        return 100 * mirror
    return find_mirror_line(transpose(block), expected_difference)

def transpose(field):
    return [[field[j][i] for j in range(len(field))] for i in range(len(field[0]))]

def run(blocks, timer):
    total = 0
    print(sum(get_block_score(b, 0) for b in blocks))
    timer.tick()
    print(sum(get_block_score(b, 1) for b in blocks))
