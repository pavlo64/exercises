import asyncio

async def countdown(n):
    while n > 0:
        yield n
        n -=1
        await asyncio.sleep(1)

async def main():
    async for number in countdown(5):
        print(number)

asyncio.run(main())