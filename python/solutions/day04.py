import re

def get_numbers(section):
    return (int(x) for x in re.findall('\d+', section))

def add_counts(cards, start, winning):
    for i in range(start + 1, min(start + winning + 1, len(cards))):
        cards[i] += cards[start]

def run(lines):
    total = 0
    cards = [1] * len(lines)
    for i, line in enumerate(lines):
        score = 0
        prefix, winning, mine = re.split('[|:]', line)
        winning_set = set(get_numbers(winning))
        matching = len([x for x in get_numbers(mine) if x in winning_set])
        if matching > 0:
            score = 2**(matching - 1)
        total += score
        add_counts(cards, i, matching)

    print(total)
    print(sum(cards))

