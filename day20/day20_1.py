import os
import time
import requests
import multiprocessing
import threading

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

url_list = [
    'https://anchorpost.msstatic.com/cdnimage/anchorpost/1080/30/9bfd4f6b8c96487580e5f09d9cfa19_2633_1701690995.jpg',
    'https://anchorpost.msstatic.com/cdnimage/anchorpost/1049/6f/12b4579a2d3b843cf3b80925b0ba64_2633_1718272873.jpg',
    'https://anchorpost.msstatic.com/cdnimage/anchorpost/1030/a8/00a66c9279f9f045b2af82d7929e18_2633_1720609774.jpg',
    'https://anchorpost.msstatic.com/cdnimage/anchorpost/1001/d7/265851d603765f16997d0f72032ceb_2633_1696647147.jpg',
    'https://live-cover.msstatic.com/huyalive/1199642599912-1199642599912-5784136945487577088-2399285323280-10057-A-0-1/20240811210336.jpg',
    'https://anchorpost.msstatic.com/cdnimage/anchorpost/1072/b8/92a70b89344e4f5b53593fa8371ea5_2633_1703571708.jpg',
    'https://anchorpost.msstatic.com/cdnimage/anchorpost/1055/bc/c2dd786f12efa3a38fb3d50984139c_2633_1722502674.jpg',
    'https://anchorpost.msstatic.com/cdnimage/anchorpost/1078/76/560fe0d50436f80d54e9ec50b361b0_6055_1720001588.jpg',
    'https://anchorpost.msstatic.com/cdnimage/anchorpost/1043/e8/2adfbc2310870db0f57d44e2287d4b_2633_1722185049.jpg',
    'https://anchorpost.msstatic.com/cdnimage/anchorpost/1089/a7/741699268c82c075b42b7b295fb714_2633_1720405483.jpg'
]
name_list = [
    'My-王劝劝【啧】',
    '被遗忘的猫幼',
    '琼明-衿衿子【白】',
    '钧木、Nuna【幸运星】',
    '琼明-星允baby',
    '琼明-菜菜要睡觉',
    '京梦-贝塔【凡尘】',
    '玲珑-Ling',
    '一只呆呆喵呀、',
    '南姿'
]


def get_data(name, url):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        with open(f'./pictures/{name}.jpg', 'wb') as f:
            f.write(response.content)


def single_process_get_data(name_lst, url_lst):
    start = time.time()

    for name, url in zip(name_lst, url_lst):
        get_data(name, url)

    end = time.time()
    print('单进程单线程花费时间：', end - start)


def multiple_process_get_data(name_lst, url_lst):
    start = time.time()
    # 创建进程数为5的进程池
    pool = multiprocessing.Pool(5)
    for name, url in zip(name_lst, url_lst):
        # 调用多进程请求数据
        pool.apply_async(get_data, args=(name, url))
    # 关闭进程池，不在接收新任务
    pool.close()
    # 等待所有进程完成
    pool.join()

    end = time.time()
    print('多进程花费时间：', end - start)


def multi_thread_get_data(name_lst, url_lst):
    start = time.time()

    thread_list = []
    for name, url in zip(name_lst, url_lst):
        # 创建多进程请求数据
        t = threading.Thread(target=get_data, args=(name, url))
        t.start()
        thread_list.append(t)
    for t in thread_list:
        t.join()

    end = time.time()
    print('单进程多线程花费时间：', end - start)


if __name__ == '__main__':
    if not os.path.exists('./pictures'):
        os.mkdir('./pictures')
    single_process_get_data(name_list, url_list)
    multiple_process_get_data(name_list, url_list)
    multi_thread_get_data(name_list, url_list)