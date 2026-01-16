import asyncio

async def simulate(num: int = 2):
    await asyncio.sleep(num)
    return num