from scratchio.scheduler import AsyncQueue, QueueClosed, Scheduler


async def producer(q, count):
    for i in range(count):
        print("Producing", i)
        q.put(i)
        await scheduler.sleep(0)

    q.close()


async def consumer(q):
    try:
        while True:
            got = await q.get()
            print("Consumed", got)
    except QueueClosed:
        return


queue = AsyncQueue()
scheduler = Scheduler()
scheduler.call_soon(producer(queue, 5))
scheduler.call_soon(consumer(queue))
scheduler.run()
