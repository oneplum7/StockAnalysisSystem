#!/usr/bin/env python
# -*- coding:utf-8 -*-

from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.mydb  
my_set = db.test_set

my_set.insert({"name":"joe001","age":3})
my_set.insert({"name":"joe002","age":4})
my_set.insert({"name":"joe003","age":5})

for i in my_set.find():
    print(i)