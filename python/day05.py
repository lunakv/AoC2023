def part_1(seeds, maps):
    src = seeds
    dst = [s for s in seeds]
    for block in maps:
        for line in block:
            dst_start, src_start, length = [int(i) for i in line.split()]
            for i, source in enumerate(src):
                if src_start <= source < src_start + length:
                    dst[i] = dst_start + source - src_start
        src = [s for s in dst]
    return min(dst)

def split(range_a, range_b):
    """Returns intersection of range_a and range_b, plus the remaining intervals from range_a"""
    s_a, e_a = range_a
    s_b, e_b = range_b
    s_i, e_i = (max(s_a, s_b), min(e_a, e_b))
    if e_i < s_i:
        return None, [range_a]
    remaining = []
    if s_a < s_b:
        remaining.append((s_a, s_b - 1))
    if e_a > e_b:
        remaining.append((e_b + 1, e_a))
    return (s_i, e_i), remaining

def part_2(seeds, maps):
    rem = seeds
    dst = []
    for block in maps:
        src, dst = dst + rem, []
        for line in block:
            rem = []
            dst_start, src_start, length = [int(i) for i in line.split()]
            src_interval = (src_start, src_start + length - 1)
            delta = dst_start - src_start
            for source in src:
                inter, remaining = split(source, src_interval)
                if inter is not None:
                    s, e = inter
                    dst.append((s + delta, e + delta))
                rem.extend(remaining)
            src = rem
        
    return min(s for s, e in src)

def run(file):
    seeds, *maps = file.split('\n\n')

    seeds = [int(s) for s in seeds.split(': ')[1].split()]
    maps = [m.split('\n')[1:] for m in maps]

    print(part_1(seeds, maps))
    seeds = [(seeds[i], seeds[i] + seeds[i+1] - 1) for i in range(0, len(seeds), 2)]
    print(part_2(seeds, maps))
