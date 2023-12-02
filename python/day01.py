import re

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
regexp = '(?=(' + "|".join(numbers) + "|[1-9]" + '))'

def convert(n):
    if n in numbers:
        return numbers.index(n) + 1
    return int(n)

total = 0
while True:
    try:
        matches = [m.group(1) for m in re.finditer(regexp, input())]
        first, last = [convert(n) for n in (matches[0], matches[-1])]
        total += 10 * first + last
    except:
        print(total)
        break



