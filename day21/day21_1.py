import time
import asyncio
import aiohttp
import aiofiles
from lxml import etree

semaphore = asyncio.Semaphore(10)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
}

async def get_img_info():
    url = 'https://sc.chinaz.com/tupian/kejijiaotongtupian.html'
    async with aiohttp.ClientSession() as session:
        async with await session.get(url, headers=headers) as response:
            response_text = await response.text()

    html = etree.HTML(response_text)
    img_url_lst = html.xpath('//div[@js-do="goPage"]/div/img/@data-original')
    img_name_lst = html.xpath('//div[@js-do="goPage"]/div/img/@alt')
    for i in range(len(img_url_lst)):
        img_url_lst[i] = 'https:' + img_url_lst[i]
    return dict(zip(img_name_lst, img_url_lst))


async def download_img(name, url):
    async with semaphore:
        start = time.time()
        async with aiohttp.ClientSession() as session:
            async with await session.get(url, headers=headers) as response:
                response_content = await response.read()

        async with aiofiles.open(f'./pictures/{name}.png', 'wb') as file:
            await file.write(response_content)
        await asyncio.sleep(1)
        end = time.time()
        print(f'{name}下载完成, 耗时{end - start}秒')


async def main():
    start = time.time()
    img_info_dict = await get_img_info()
    task_lst = []
    for name, url in img_info_dict.items():
        task = asyncio.create_task(download_img(name, url))
        task_lst.append(task)
    await asyncio.wait(task_lst)
    end = time.time()
    print(f'所有文件下载完成, 总共耗时{end - start}秒')



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    # asyncio.run(main())
