import asyncio
import time

async def delayed_hello(name, delay):
    await asyncio.sleep(delay)
    return f"Hello, {name}"

async def main():
    result = await delayed_hello("Pavlo", 2)
    print(result)

if __name__ == "__main__":
    print(time.time())
    asyncio.run(main())
    print(time.time())