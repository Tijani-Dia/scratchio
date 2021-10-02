import pytest

from scratchio.async_queue import AsyncQueue
from scratchio.scheduler import Scheduler


@pytest.mark.asyncio
async def test_empty():
    q = AsyncQueue()
    assert q.is_empty()
    q.put(1)
    assert not q.is_empty()
    assert await q.get() == 1
    assert q.is_empty()


@pytest.mark.asyncio
async def test_order():
    q = AsyncQueue()
    for i in [1, 3, 2]:
        q.put(i)

    items = [await q.get() for _ in range(3)]
    assert items == [1, 3, 2]


@pytest.mark.asyncio
async def test_get():
    q = AsyncQueue()
    scheduler = Scheduler()
    q.put(1)
    got = []

    async def queue_get():
        got.append(await q.get())

    scheduler.call_soon(queue_get())
    scheduler.run()
    assert got == [1]
