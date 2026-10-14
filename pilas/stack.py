class Stack:
    def __init__(self, capacity):
        self.items = []
        self.capacity = capacity

    def push(self, item):
        if self.is_full():
            return False

        self.items.append(item)
        return True

    def pop(self):
        if self.is_empty():
            return None

        return self.items.pop()

    def peek(self):
        if self.is_empty():
            return None

        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def is_full(self):
        return len(self.items) >= self.capacity

    def get_items(self):
        return self.items