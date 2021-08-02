import heapq
import time
import types
from collections import deque


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
    def _sleep(self):
        yield

    async def sleep(self, delay):
        when = time.monotonic() + delay
        self.call_at(self.ready.popleft(), when)
        await self._sleep()

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
                    self.ready.popleft()

            if not self.scheduled and not self.ready:
                return
