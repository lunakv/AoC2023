
def parse(file, mode):
    if mode == 'lines':
        return parse_lines(file)
    if mode == 'splitlines':
        return parse_splitlines(file)
    if mode == 'intlines':
        return parse_intlines(file)
    if mode == 'blocks':
        return parse_blocks(file)
    if mode == 'rawblocks':
        return parse_rawblocks(file)
    if mode == 'intblocks':
        return parse_intblocks(file)
    return parse_file(file)

def parse_lines(file):
    return parse_file(file).split('\n')

def parse_blocks(file):
    return [block.split('\n') for block in parse_rawblocks(file)]

def parse_rawblocks(file):
    return parse_file(file).split('\n\n')

def parse_intlines(file):
    return [line_to_ints(l) for l in parse_lines(file)]

def parse_intblocks(file):
    return [[line_to_ints(l) for l in b] for b in parse_blocks(file)]

def parse_splitlines(file):
    return [line.split() for line in parse_lines(file)]

def parse_file(file):
    return file.strip()

def line_to_ints(line):
    return [int(d) for d in line.split()]
