from time import perf_counter_ns

class Timer:
    def __init__(self):
        self.times = []

    def tick(self):
        self.times.append(perf_counter_ns())

    def intervals(self):
        return [self.times[i] - self.times[i-1] for i in range(1, len(self.times))]

    def total_time(self):
        if not self.times:
            return 0

        return self.times[-1] - self.times[0]

    def __str__(self):
        total = format_interval(self.total_time())
        if len(self.times) > 2:
            intervals = ' (' + ', '.join(format_interval(i) for i in self.intervals()) + ')'
        else:
            intervals = ''

        return f"{total}{intervals}"


def format_interval(interval):
    suffixes = [('ns', 1000), ('us', 1000), ('ms', 1000), ('s', 60), ('m', 60), ('h', None)]
    
    i = 0
    rem = 0
    while i < len(suffixes):
        suffix, divisor = suffixes[i]
        if divisor is not None and interval > divisor:
            interval, rem = divmod(interval, divisor)
            i += 1
        else:
            break

    if interval < 10 and i > 0: 
        prev = suffixes[i-1]
        if i > 3:
            # 1m30s
            return f"{interval}{suffix}{rem}{prev[0]}"
        else:
            # 1.8s
            return f"{interval}.{rem * 10 // prev[1]}{suffix}"

    return f"{interval}{suffix}"

