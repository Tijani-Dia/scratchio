import heapq
import time
import types
from collections import deque


class QueueClosed(Exception):
    pass


class AsyncQueue:
    def __init__(self, scheduler):
        self.scheduler = scheduler
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
            self.scheduler.call_later(self.scheduler.ready.popleft(), 0)
            yield


class Scheduler:
    sequence = 0

    def __init__(self):
        self.ready = deque()
        self.scheduled = list()

    def call_soon(self, coro):
        self.ready.append(coro)

    def call_later(self, coro, delay):
        when = time.monotonic() + delay
        self.call_at(coro, when)

    def call_at(self, coro, when):
        self.sequence += 1
        heapq.heappush(self.scheduled, (when, self.sequence, coro))

    @types.coroutine
    def sleep(self, delay):
        when = time.monotonic() + delay
        self.call_at(self.ready.popleft(), when)
        yield

    def run(self):
        while True:
            while self.scheduled:
                deadline, _, coro = self.scheduled[0]
                now = time.monotonic()
                if deadline > now:
                    break

                self.ready.append(heapq.heappop(self.scheduled)[2])

            while self.ready:
                coro = self.ready[0]
                try:
                    coro.send(None)
                except StopIteration:
                    try:
                        self.ready.popleft()
                    except:
                        pass

            if not self.scheduled and not self.ready:
                return
