import re
from math import prod
from collections import defaultdict


def get_symbols(string):
    return list(re.finditer(r'[^\d.]+', string))

def get_numbers(string):
    return list(re.finditer(r'\d+', string))

def overlaps(number, symbol):
    s = symbol.start()
    if s < number.start() - 1:
        return -1
    elif s <= number.end():
        return 0
    else:
        return 1

def find_overlaps(numbers, symbols):
    i = 0
    for num in numbers:
        while i < len(symbols):
            cmp = overlaps(num, symbols[i])
            if cmp == 0:
                yield num, symbols[i]
                break
            if cmp == 1:
                break
            i += 1

def parse_board(board):
    number_map, symbol_map = defaultdict(set), defaultdict(set)
    symbols_above = []
    symbols_on_line = get_symbols(board[0])
    for line in range(len(board)-1):
        numbers_on_line = get_numbers(board[line])
        symbols_below = get_symbols(board[line+1])

        for d, symbols in enumerate((symbols_above, symbols_on_line, symbols_below)):
            for overlap_n, overlap_s in find_overlaps(numbers_on_line, symbols):
                num_key = (line + d - 1, overlap_n.start(), int(overlap_n.group()))
                sym_key = (line + d - 1, overlap_s.start(), overlap_s.group())
                number_map[num_key].add(sym_key)
                symbol_map[sym_key].add(num_key)

        symbols_above = symbols_on_line
        symbols_on_line = symbols_below
    return number_map, symbol_map

def run(file):
    board = [l.strip() for l in file.split('\n')]
    board.append('.'*len(board[0]))

    numbers, symbols = parse_board(board)
    total = sum(nk[2] for nk in numbers.keys())
    print(total)

    gear_ratios = sum(prod(nk[2] for nk in symbols[g]) for g in symbols if g[2] == '*' and len(symbols[g]) == 2)
    print(gear_ratios)
