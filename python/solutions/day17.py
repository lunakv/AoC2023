class PriorityQueue:
    def __init__(self, initial):
        if not initial:
            self.heap = []
        else:
            self.heap = [i.copy() for i in initial]

        self.size = len(self.heap)
        self.item_pointers = {self.heap[i][1]: i for i in range(self.size)}
        self._heapify()

    def empty(self):
        return self.size == 0

    def insert(self, item, priority):
        self.size += 1
        self.heap.append([priority, item])
        self.item_pointers[item] = self.size - 1
        self._bubble_up(self.size - 1)

    def decrease(self, item, priority):
        i = self.item_pointers[item]
        old_prio = self.heap[i][0] 
        self.heap[i][0] = priority
        self._bubble_up(i)

    def insert_or_decrease(self, item, priority):
        if item in self.item_pointers:
            self.decrease(item, priority)
        else:
            self.insert(item, priority)

    def extract_min(self):
        top = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        del self.item_pointers[top[1]]
        self.size -= 1
        self._bubble_down(0)
        return top

    def _parent(self, i): 
        return (i - 1)//2

    def _min_child(self, i):
        c = 2 * i + 1
        if c >= self.size:
            return None
        if c + 1 < self.size and self.heap[c + 1] < self.heap[c]:
            return c + 1
        return c

    def _bubble_up(self, i):
        while i > 0:
            p = self._parent(i)
            if self.heap[p] <= self.heap[i]:
                return
            self._swap(p, i)
            i = p

    def _bubble_down(self, i):
        c = self._min_child(i)
        while c and self.heap[i] > self.heap[c]:
            self._swap(i, c)
            i = c
            c = self._min_child(i)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.item_pointers[self.heap[i][1]] = i
        self.item_pointers[self.heap[j][1]] = j

    def _heapify(self):
        for i in range(self.size // 2 - 1, -1, -1):
            self._bubble_down(i)

        
class Crucible:
    dirs = ['U', 'R', 'D', 'L']
    steps = {'U': (-1, 0), 'R': (0, +1), 'D': (1, 0), 'L': (0, -1)}

    def __init__(self, grid):
        self.grid = [[int(c) for c in line] for line in grid]
        self.height = len(self.grid)
        self.width = len(self.grid[0])

    def starts(self):
        # [[edge_length, (x, y, direction, path_length)]]
        return [[self.grid[0][1], (0, 1, 'R', 1)], [self.grid[1][0], (1, 0, 'D', 1)]]

    def is_end(self, item):
        return item[0] == self.height - 1 and item[1] == self.width - 1

    def inside_grid(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width

    def neighbors(self, step):
        x, y, direction, length = step
        for new_dir, new_len in self._next_paths(direction, length):
            dx, dy = Crucible.steps[new_dir]
            nx, ny = x + dx, y + dy
            if self.inside_grid(nx, ny):
                yield self.grid[nx][ny], (nx, ny, new_dir, new_len)

    def _next_paths(self, direction, length):
        if self._can_step_forward(direction, length):
            yield direction, length + 1
        if self._can_step_sideways(direction, length):
            right = (Crucible.dirs.index(direction) + 1) % 4
            left = (Crucible.dirs.index(direction) + 3) % 4
            yield Crucible.dirs[right], 1
            yield Crucible.dirs[left], 1

    def _can_step_forward(self, direction, length):
        return length < 3

    def _can_step_sideways(self, direction, length):
        return True

class UberCrucible(Crucible):
    def is_end(self, item):
        return super().is_end(item) and self._can_step_sideways(item[2], item[3])

    def _can_step_forward(self, direction, length):
        return length < 10

    def _can_step_sideways(self, direction, length):
        return length >= 4


def dijkstra(starts, is_end, neighbors):
    opened = PriorityQueue(starts)
    distances = {s[1]: s[0] for s in starts}

    while not opened.empty():
        distance, item  = opened.extract_min()
        if is_end(item):
            return distances, item 

        for edge_length, neighbor in neighbors(item):
            new_distance = distance + edge_length
            if neighbor in distances and distances[neighbor] <= new_distance:
                continue
            distances[neighbor] = new_distance
            opened.insert_or_decrease(neighbor, new_distance)


def run(lines, timer):
    crucible = Crucible(lines)
    lengths, end = dijkstra(crucible.starts(), crucible.is_end, crucible.neighbors)
    print(lengths[end])

    timer.tick()

    uber = UberCrucible(lines)
    lengths, end = dijkstra(uber.starts(), uber.is_end, uber.neighbors)
    print(lengths[end])

