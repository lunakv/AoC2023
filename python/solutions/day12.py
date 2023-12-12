from functools import cache

@cache
def get_combinations(string, signature, in_block=False):
    if not signature or signature == (0,):
        return all(c != '#' for c in string)
    if not string:
        return not signature or signature == (0,)
    
    head, *tail = string
    sig_head, *sig_tail = signature
    total = 0
    if head != '.' and sig_head > 0:
        total += get_combinations(string[1:], (sig_head-1, *sig_tail), True)
    if head != '#' and (not in_block or sig_head == 0):
        total += get_combinations(string[1:], signature[in_block:], False)
    return total

def run(lines):
    total_1 = 0
    total_2 = 0
    for line in lines:
        layout, signature = line.split()
        signature = tuple(int(s) for s in signature.split(','))
        total_1 += get_combinations(layout, signature)
        total_2 += get_combinations('?'.join([layout]*5), signature*5)

    print(total_1)
    print(total_2)

