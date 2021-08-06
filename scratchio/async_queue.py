import types
from collections import deque


class QueueClosed(Exception):
    pass


class AsyncQueue:
    def __init__(self):
        self.items = deque()
        self.closed = False

    def is_empty(self):
        return not bool(self.items)

    def close(self):
        self.closed = True

    def put(self, item):
        if self.closed:
            raise QueueClosed

        self.items.append(item)

    @types.coroutine
    def get(self):
        while True:
            if self.items:
                return self.items.popleft()
            if self.closed:
                raise QueueClosed
            yield
