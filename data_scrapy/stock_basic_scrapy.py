# -*- coding: utf-8 -*-
# author:           oneplum7
# create_time:      2020/10
# file_name:        rightview.py
# github           https://github.com/oneplum7?tab=repositories
# qq邮箱            2104878583@qq.com


import requests

import pymongo


client = pymongo.MongoClient(host="localhost",port=27017)
#client = pymongo.MongoClient('mongodb://zero:123@localhost:27017/')

db = client['stock']
table_basic = db['basic']

myquery = {"code":603259}
newvalue = {"$set":{"location":"上海","name":"宁德","code":"300750"}}
#table_basic.delete_one(myquery)
res = table_basic.update_one(myquery, newvalue, True)
#res = table_basic.update_one({'code':code}, {'$set': data}, True)
for x in table_basic.find():
      print(x)

# from lxml import etree
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
# }

# #response = requests.get(url='http://quote.eastmoney.com/stock_list.html',headers=headers)
# response = requests.get(url='http://quote.eastmoney.com/center/gridlist.html#hs_a_board',headers=headers)

# html = etree.HTML(response.text.encode(response.encoding).decode('gbk','ignore'))

# location = '上海'

# print(len(html.xpath('//div[@id="quotesearch"]/ul/li/a/text()')))

# for stock in html.xpath('//div[@id="quotesearch"]/ul/li/a/text()'):
#     left = stock.index('(')
#     name = stock[0:left]
#     code = stock[left+1:-1]
#     if name=='宁德时代':
#         location = '深圳'
#         print(name,code)
#     data = {
#         'location':location,
#         'name':name,
#         'code':code
#     }
#     # 上海和深圳可能有两个同名的股票
#     # 上海股市也可能有同名股票，但是code不一样
#     res = table_basic.update_one({'code':code}, {'$set': data}, True)
#     if res.modified_count>0:
#         print(name,code)

