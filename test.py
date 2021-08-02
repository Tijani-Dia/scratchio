from scratchio.scheduler import Scheduler

scheduler = Scheduler()


async def first():
    print("On first scheduled")
    await scheduler.sleep(2)
    print("Finished first scheduled")


async def second():
    print("On second scheduled")
    await scheduler.sleep(1)
    print("Finished second scheduled")


async def main():
    print("On main")
    scheduler.call_soon(first())
    scheduler.call_soon(second())
    print("Quitting main")


scheduler.call_soon(main())
scheduler.run()
