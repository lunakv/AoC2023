face_cards = ['T', 'J', 'Q', 'K', 'A']

def parse_line(tokens):
    cards, bet = tokens
    bet = int(bet)
    cards = [face_cards.index(c) + 10 if c in face_cards else int(c) for c in cards]
    return cards, bet

def counts(lst):
    seen = set()
    jokers = 0
    cnts = []
    for el in lst:
        if el == 0:
            jokers += 1
        elif el not in seen:
            cnts.append(lst.count(el))
            seen.add(el)
    cnts.sort(reverse=True)
    if len(cnts) == 0:
        return [5]
    cnts[0] += jokers
    return cnts

def hand_key(hand):
    return tuple(counts(hand[0]) + hand[0])

def replace_jokers(hand):
    cards, bet = hand
    return [0 if c == 11 else c for c in cards], bet

def score(hands):
    return sum(i * bet for i, (_, bet) in enumerate(hands, start=1))

def run(splitlines):
    hands = sorted(map(parse_line, splitlines), key=hand_key)
    print(score(hands))
    hands = sorted(map(replace_jokers, hands), key=hand_key)
    print(score(hands))

