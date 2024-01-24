import aiohttp
import asyncio
import time
from task_4_1 import urls
import os
import aiofiles


async def download_as(url):
    folder = 'data_asyncio'
    if not os.path.exists(folder):
        os.mkdir(folder)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as responce:
            extention = responce.headers.get('Content-Type').split('/')[1]
            url = url.split('?')
            url = url[0].split('/')
            url = url[-1].replace('.jpeg','')
            async with aiofiles.open(f'{folder}/{url}.{extention}','wb') as f:
                start_time = time.time()
                await f.write(await responce.read())
                print(f'Скачивание  изображения выполнено за {time.time() - start_time:2f} секунд')

async def main():
    start_time = time.time()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download_as(url))
        tasks.append(task)
        await asyncio.gather(*tasks)
    print(f'Скачивание  всех изображений выполнено за {time.time() - start_time:2f} секунд')




if __name__ == '__main__':
    asyncio.run(main())
