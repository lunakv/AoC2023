from math import prod

def get_counts(pull):
    return {name: int(count) for count, name in [comp.split(" ") for comp in pull.split(", ")]} 
        
def max_pull(pulls):
    m = {"red":0, "green":0, "blue":0}
    for c in pulls:
        for key in c:
            m[key] = max(m[key], c[key])
    return m

def run(lines):
    limits = {"red":12, "green":13, "blue":14}
    i = 0
    total = 0
    power = 0
    for line in lines:
        i += 1
        line = line.split(": ")[1]
        m = max_pull(get_counts(turn) for turn in line.split("; "))
        if all(m[k] <= limits[k] for k in limits):
            total += i
        power += prod(m.values())
    print(total)
    print(power)

