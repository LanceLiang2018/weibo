import pymongo
import json
from tqdm import trange
from bs4 import BeautifulSoup as Soup


errors = []


def output(conclude: list):
    with open('你好明天(GBK).txt', 'w', encoding='GBK') as f:
        for i in conclude:
            f.write(i['created_at'] + '\n')
            f.write(i['text'] + '\n\n')
    with open('你好明天(UTF8).txt', 'w', encoding='UTF-8') as f:
        for i in conclude:
            f.write(i['created_at'] + '\n')
            f.write(i['text'] + '\n\n')


def output2(conclude: list):
    try:
        with open('ALL(GBK).txt', 'w', encoding='GBK') as f:
            for i in conclude:
                f.write(i['created_at'] + '\n')
                f.write(i['text'] + '\n\n')
    except UnicodeEncodeError:
        pass
    with open('ALL(UTF8).txt', 'w', encoding='UTF-8') as f:
        for i in conclude:
            f.write(i['created_at'] + '\n')
            f.write(i['text'] + '\n\n')


def parse_card(card: dict):
    # print(card)
    try:
        mblog = card['mblog']
        created_at = mblog['created_at']
        # if '-' in created_at:
        #     created_at = (created_at.replace('-', '月')) + '日'
        #     s = created_at.spilt('-')
        #     if len(s) == 3
        # print(created_at)
        html = mblog['text']
        soup = Soup(html, 'html.parser')
        text = soup.get_text()
        text = text.replace('...全文', '')

        if '#你好，明天#' in text:
            text = text.replace('【#你好，明天#】', '')
            # print(created_at, text)
            return {
                'created_at': created_at,
                'text': text
            }
        return None

    except KeyError:
        return None


def parse_card2(card: dict):
    # print(card)
    try:
        mblog = card['mblog']
        created_at = mblog['created_at']
        # if '-' in created_at:
        #     created_at = (created_at.replace('-', '月')) + '日'
        #     s = created_at.spilt('-')
        #     if len(s) == 3
        # print(created_at)
        html = mblog['text']
        soup = Soup(html, 'html.parser')
        text = soup.get_text()
        text = text.replace('...全文', '')

        return {
            'created_at': created_at,
            'text': text
        }

    except KeyError:
        return None


def parse_page(page):
    data = db.find_one({'page': page})
    if data is None:
        # raise ValueError
        errors.append(page)
        # print("ERROR:", page)
        return
    # print(data)
    # soup = Soup(data['text'], 'html.parser')
    js = json.loads(data['text'])
    cards = js['data']['cards']
    results = []
    for card in cards:
        res = parse_card2(card)
        if res is None:
            continue
        results.append(res)
    return results


def main():
    ranging = (1, 2000)
    conclude = []
    for mpage in trange(ranging[0], ranging[1]):
        results = parse_page(mpage)
        if results is None:
            continue
        conclude.extend(results)
    # print(conclude)
    output2(conclude)


manager = pymongo.MongoClient()
db = manager.weibo.weibo3


if __name__ == '__main__':
    main()