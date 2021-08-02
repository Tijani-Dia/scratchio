from scratchio.scheduler import AsyncQueue, QueueClosed, Scheduler

scheduler = Scheduler()
queue = AsyncQueue(scheduler)


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
    except QueueClosed:
        return


scheduler.call_soon(producer(queue, 5))
scheduler.call_soon(consumer(queue))
scheduler.run()