import pymongo
import json
from tqdm import trange
# from bs4 import BeautifulSoup as Soup


errors = []


def parse_one(page):
    data = db.find_one({'page': page})
    if data is None:
        # raise ValueError
        errors.append(page)
        print("ERROR:", page)
        return
    # print(data)
    # soup = Soup(data['text'], 'html.parser')
    js = json.loads(data['text'])
    print(js['data']['cards'])


def main():
    ranging = (1, 1000)
    for mpage in trange(ranging[0], ranging[1]):
        parse_one(mpage)


manager = pymongo.MongoClient()
db = manager.weibo.weibo2


if __name__ == '__main__':
    main()