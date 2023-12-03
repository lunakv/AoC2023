import re

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
regexp = '(?=(' + "|".join(numbers) + "|[1-9]" + '))'

def convert(n):
    if n in numbers:
        return numbers.index(n) + 1
    return int(n)

def run(file):
    total = 0
    for line in file.split('\n'):
        matches = [m.group(1) for m in re.finditer(regexp, line)]
        first, last = [convert(n) for n in (matches[0], matches[-1])]
        total += 10 * first + last
    print(total)

