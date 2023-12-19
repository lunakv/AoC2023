import re

def get_hash(string):
    value = 0
    for c in string:
        value += ord(c)
        value *= 17
        value %= 256
    return value

class LightBoxes:
    def __init__(self):
        self.labels = []
        self.lights = []
        for _ in range(256):
            self.labels.append([])
            self.lights.append([])

    def set_light(self, box, label, value):
        try:
            index = self.labels[box].index(label)
            self.lights[box][index] = value
        except ValueError:
            self.labels[box].append(label)
            self.lights[box].append(value)

    def delete_light(self, box, label):
        try:
            index = self.labels[box].index(label)
            del self.labels[box][index]
            del self.lights[box][index]
        except ValueError:
            pass

    def get_value(self):
        return sum((i+1) * self.get_box_value(box) for i, box in enumerate(self.lights))

    def get_box_value(self, box):
        return sum((i+1) * int(value) for i, value in enumerate(box))

def run(file, timer):
    print(sum(map(get_hash, file.split(','))))

    timer.tick()

    boxes = LightBoxes()
    for token in file.split(','):
        m = re.search(r"(\w+)([=-])(\d)?", token)
        label = m.group(1)
        symbol = m.group(2)
        box = get_hash(label)
        if symbol == '-':
            boxes.delete_light(box, label)
        else:
            boxes.set_light(box, label, m.group(3))

    print(boxes.get_value())

