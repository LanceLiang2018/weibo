import requests
import json
import threading
import queue
import pymongo
from tqdm import trange
# from retrying
import time


surl = 'https://m.weibo.cn/api/container/getIndex?uid=2803301701&luicode=10000011&lfid=100103type%3D1%26q%3D%E4%BA%BA%E6%B0%91%E6%97%A5%E6%8A%A5&featurecode=20000320&type=uid&value=2803301701&containerid=1076032803301701&page='
timeout = 1
delay = 1.5


def fetch_one(page):
    target = page
    url = surl + str(target)
    try:
        resp = requests.get(url, timeout=timeout)
    except requests.exceptions.ReadTimeout:
        return False
    # print(resp.text)

    try:
        js = json.loads(resp.text)
    except json.decoder.JSONDecodeError:
        return False

    db.insert_one({
        'page': page,
        'text': resp.text
    })
    return True


def main():
    errors = []
    ranging = (1, 10000)
    now = ranging[0]
    for _ in trange(ranging[0], ranging[1]):
        mpage = now
        time.sleep(delay)
        result = fetch_one(mpage)
        if result is False:
            errors.append(mpage)
            print('ERROR:', mpage)
            continue
        now = now + 1
    print('ERRORS:', errors)


def test(page=1):
    # 在这里先测试一下
    target = page
    url = surl + str(target)
    resp = requests.get(url, timeout=timeout)
    # print(resp.text)


q = queue.Queue()
manager = pymongo.MongoClient()
db = manager.weibo.weibo2
db.drop()


if __name__ == '__main__':
    main()
    # test()
    # for i in trange(1, 1000):
    #     test(i)