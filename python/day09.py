
def run(file):
    lines = [[int(d) for d in l.split()] for l in file.split('\n')]

    part_1 = 0
    part_2 = 0
    for line in lines:
        last, first = 0, 0
        sign = 1
        diffs = line
        while not all(d == 0 for d in diffs):
            last += diffs[-1]
            first += diffs[0] * sign
            sign *= -1
            diffs = [diffs[i]-diffs[i-1] for i in range(1, len(diffs))]
        part_1 += last 
        part_2 += first

    print(part_1)
    print(part_2)

