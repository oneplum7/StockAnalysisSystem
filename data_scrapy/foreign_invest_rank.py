import requests

from lxml import etree

import myDict

import pymongo

client = pymongo.MongoClient(host="localhost",port=27017)
db = client['stock']
table_basic = db['basic']

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}

base_url = 'http://data.eastmoney.com/hsgt/index.html'

response = requests.get(url=base_url,headers=headers)

html = etree.HTML(response.text)
#for tr in html.xpath('//table[@class="tab1"]/tr'):
print(len(html.xpath('//div[@id="tb_hsgtsdjcsj"]/ul/li/a/text()')))
print(len(html.xpath('//table[@class="tab1"]/tr')))
for tr in html.xpath('//div[@id="tb_hsgtsdjcsj"]/ul/li/a/text()'):
    tds = tr.xpath('.//td/text()')
    code,stock_name,current_price,quote_change = tds[1],tds[2],tds[4],tds[5]
    net_purchase, buy_in, buy_out, turnover = tds[6],tds[7],tds[8],tds[9]
    print(code,stock_name,current_price,quote_change,net_purchase, buy_in, buy_out, turnover)

    data = {
        'code': code,
        'stock_name': stock_name,
        'current_price': current_price,
        'quote_change': quote_change,
        'net_purchase': net_purchase,
        'buy_in': buy_in,
        'buy_out': buy_out,
        'turnover': turnover,
    }
    #table_quotes.update_one({'code': code}, {'$set': data}, True)