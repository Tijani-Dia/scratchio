import time
import types
from collections import deque

from .queues import PriorityQueue

SLEEPING = "__sleeping__"


class QueueClosed(Exception):
    pass


class AsyncQueue:
    def __init__(self):
        self.items = deque()
        self.closed = False

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


class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.scheduled = PriorityQueue()
        self.current = None

    def call_soon(self, coro):
        self.ready.append(coro)

    def call_later(self, coro, delay):
        when = time.monotonic() + delay
        self.call_at(coro, when)

    def call_at(self, coro, when):
        self.scheduled.insert_item_with_priority(item=coro, priority=when)

    @types.coroutine
    def sleep(self, delay):
        when = time.monotonic() + delay
        self.call_at(self.current, when)
        yield SLEEPING

    def run(self):
        while True:
            while self.ready:
                self.current = self.ready.popleft()
                try:
                    result = self.current.send(None)
                except StopIteration:
                    continue
                else:
                    if result == SLEEPING:
                        continue
                    self.call_later(self.current, 0)
            self.current = None

            while not self.scheduled.is_empty():
                item = self.scheduled.peek()
                now = time.monotonic()
                if item.priority > now:
                    break

                hp_item = self.scheduled.pull_highest_pritority_item()
                self.ready.append(hp_item)

            if self.scheduled.is_empty() and not self.ready:
                return
