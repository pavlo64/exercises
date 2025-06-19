import asyncio
async def slow_op():
    await asyncio.sleep(2)
    return "Completed!"

def report_done(task):
    print("Task done with result:", task.result())

async def main():
    task = asyncio.create_task(slow_op())
    task.add_done_callback(report_done)
    await task

asyncio.run(main())
