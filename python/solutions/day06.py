from math import floor, ceil, sqrt

def get_beat_count(t, d):
    discriminant = sqrt(t**2 - 4*d)
    soonest = floor((t-discriminant)/2) + 1
    latest = ceil((t+discriminant)/2) - 1
    return latest - soonest + 1

def run(lines, timer):
    times = [int(x) for x in lines[0].split(':')[1].split()]
    distances = [int(x) for x in lines[1].split(':')[1].split()]

    product = 1
    for t, d in zip(times, distances):
        product *= get_beat_count(t, d)
    print(product)

    timer.tick()
    time = int(''.join(str(t) for t in times))
    distance = int(''.join(str(d) for d in distances))
    print(get_beat_count(time, distance))

