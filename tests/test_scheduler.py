import time

from scratchio import Scheduler


def test_run():
    count = 0
    scheduler = Scheduler()

    async def callback():
        nonlocal count
        count += 1

    scheduler.call_soon(callback())
    scheduler.run()
    assert count == 1


def test_run_2():
    scheduler = Scheduler()

    t0 = time.monotonic()
    scheduler.call_soon(scheduler.sleep(0.1))
    scheduler.run()
    t1 = time.monotonic()
    assert 0.1 <= t1 - t0 <= 0.2


def test_call_later():
    scheduler = Scheduler()
    results = []

    async def callback(arg):
        results.append(arg)

    scheduler.call_later(callback("hello world"), 0.1)
    scheduler.run()
    assert results == ["hello world"]


def test_call_soon():
    scheduler = Scheduler()
    results = []

    def callback(arg1, arg2):
        results.append(arg1)
        yield
        results.append(arg2)

    scheduler.call_soon(callback("hello", "world"))
    scheduler.run()
    assert results == ["hello", "world"]
