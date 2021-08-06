from scratchio.scheduler import AsyncQueue, QueueClosed, Scheduler


async def producer(q, count):
    for i in range(count):
        print("Producing", i)
        q.put(i)
        await scheduler.sleep(1)

    q.close()


async def consumer(q):
    try:
        while True:
            got = await q.get()
            print("Consumed", got)
            await scheduler.sleep(0.5)
    except QueueClosed:
        return


async def consumer2(q):
    try:
        while True:
            got = await q.get()
            print("2 Consumed", got)
            await scheduler.sleep(0.5)
    except QueueClosed:
        return


queue = AsyncQueue()
scheduler = Scheduler()
scheduler.call_soon(producer(queue, 5))
scheduler.call_soon(consumer(queue))
scheduler.call_soon(consumer2(queue))
scheduler.run()
