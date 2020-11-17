import tushare as ts
import myDict

import pymongo

client = pymongo.MongoClient(host="localhost",port=27017)
db = client['stock']
table_basic = db['basic']

# pro = ts.pro_api('081f3bb7aa5a6142a95dc8c2c51a75428c898d3fc1fa0fa87e0974f5')
# data = pro.hsgt_top10(trade_date='20101027', market_type='1')

table_quotes = db['hgt'+'_' + '20101027']

import akshare as ak
stock_em_hsgt_south_acc_flow_in_df = ak.stock_em_hsgt_south_acc_flow_in(indicator="沪股通")
print(stock_em_hsgt_south_acc_flow_in_df)


# for row in data:
#     trade_date = row[0]
#     ts_code = row[1]
#     name = row[2]
#     close =row[3]
#     change = row[4]
#     rank = row[5]
#     market_type = row[6]
#     amount =row[7]
#     net_amount =  row[8]
#     buy = row[9]
#     sell = row[10]
#     print(trade_date, ts_code)
    # data = {
    #     'trade_date': trade_date,
    #     'ts_code': ts_code,
    #     'name': name,
    #     'close': close,
    #     'net_purchase': net_purchase,
    #     'buy_in': buy_in,
    #     'buy_out': buy_out,
    #     'turnover': turnover,
    # }
    # column_list.append(row)