import asyncio
async def fetch(url):
    await asyncio.sleep(1)
    return f"Данные с {url}"

async def main():
    urls = ["https://site1.com", "https://site2.com", "https://site3.com"]
    tasks = [asyncio.create_task(fetch(url)) for url in urls]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
