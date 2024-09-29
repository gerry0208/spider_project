import asyncio
import json
import time

import aiofiles
import aiohttp
from lxml import etree
from urllib import parse


# 字段转换
async def convert_field(field):
    field = field.encode('utf-8')
    field = field.decode('utf-8').replace('\\x', '%')
    field = parse.unquote(field)
    return field


# 抓取数据
async def get_data(url):
    async with aiohttp.ClientSession() as session:
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'Accept-Language': "zh-CN,zh;q=0.9",
            'Cache-Control': "max-age=0",
            'Upgrade-Insecure-Requests': "1",
            'Cookie': "acw_tc=0a47318317266683125558638e00389119b14cb190fc66f74b0d7aea3cfe79; mcb9_2132_saltkey=tS59sira; mcb9_2132_lastvisit=1726664716; mcb9_2132_sid=WPNPuh; mcb9_2132_pc_size_c=0; mcb9_2132_atarget=1; mcb9_2132_visitedfid=425; mcb9_2132_gfcity=430; _uab_collina=172666831941547716698115; qimo_seosource_0=%E7%AB%99%E5%86%85; qimo_seokeywords_0=; uuid_994d4130-1df9-11e9-b7ec-7766c2691ec6=322624c5-3c1c-4e66-bfaf-d9174c7b9bdb; qimo_seosource_994d4130-1df9-11e9-b7ec-7766c2691ec6=%E7%AB%99%E5%86%85; qimo_seokeywords_994d4130-1df9-11e9-b7ec-7766c2691ec6=; qimo_xstKeywords_994d4130-1df9-11e9-b7ec-7766c2691ec6=; href=http%3A%2F%2Fbbs.itheima.com%2Fforum-425-1.html; accessId=994d4130-1df9-11e9-b7ec-7766c2691ec6; Hm_lvt_7ea6c0c8412eb91d6e44a2459dc4ae81=1726668320; HMACCOUNT=ADC18AC9C778FEDD; UM_distinctid=1920573ad361580-0587cb2997825c-26001151-2cdb94-1920573ad3713f3; mcb9_2132_sendmail=1; mcb9_2132_st_t=0%7C1726668368%7Cc46b49f3d212f5f2e76cad32667360ac; mcb9_2132_forum_lastvisit=D_425_1726668368; Hm_lpvt_7ea6c0c8412eb91d6e44a2459dc4ae81=1726668372; CNZZDATA3092227=cnzz_eid%3D959992546-1726668320-%26ntime%3D1726668372; pageViewNum=2; mcb9_2132_lastact=1726668404%09forum.php%09ajax"
        }

        async with session.get(url, headers=headers) as response:
            content = await response.read()
            text = str(content)

        await asyncio.sleep(2)

    # 解析字段
    html = etree.HTML(text)
    title_list = html.xpath('//table[@summary="forum_425"]/tbody/tr/th/a[1]/text()')
    url_list = html.xpath('//table[@summary="forum_425"]/tbody/tr/th/a[1]/@href')
    name_list = html.xpath('//table[@summary="forum_425"]/tbody/tr/th/div/i/a/span/text()')
    time_list = html.xpath('//table[@summary="forum_425"]/tbody/tr/th/div/i/span[1]/text()')
    item_list = []
    for title, urls, name, times in zip(title_list, url_list, name_list, time_list):
        title = await convert_field(title)
        urls = await convert_field(url)
        name = await convert_field(name)
        times = await convert_field(times)
        times = times.lstrip('@ ')
        item = {'文章标题': title, '文章作者': name, '文章链接': urls, '发布时间': times}
        item_list.append(item)

    # 存入文件
    async with aiofiles.open('张昊明.json', 'a', encoding='utf-8') as file:
        await file.write(json.dumps(item_list, ensure_ascii=False))


page = input('请输入抓取页号，用空格分隔：')
page_list = page.split(' ')

# 创建协程任务
tasks = []
for page in page_list:
    url = f"http://bbs.itheima.com/forum-425-{page}.html"
    task = asyncio.ensure_future(get_data(url))
    tasks.append(task)
    print(f'正在抓取第{page}页...')

loop = asyncio.get_event_loop()
start = time.time()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()
print('协程消耗时间', end - start)
loop.close()
