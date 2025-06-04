import asyncio
import time

async def delayed_hello(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"Hello, {name}"

async def main():
    start = time.time()
    task1 = asyncio.create_task(delayed_hello('Pavlo', 2))
    task2 = asyncio.create_task(delayed_hello('Oleksandr', 3))
    task3 = asyncio.create_task(delayed_hello('Tetiana', 1))
    result1 = await task1
    result2 = await task2
    result3 = await task3
    end = time.time()
    print(result1)
    print(result2)
    print(result3)
    print(f"Executed in {end - start:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(main())