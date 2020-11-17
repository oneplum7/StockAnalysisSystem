import mysql.connector


#连接数据库
# 获取操作游标
#创建数据库表
#存储过程 
#关闭数据库


# mydb = mysql.connector.connect(host="localhost",user="root",password="gziscas",database="mydatabase",charset='utf8')
#         mycursor = mydb.cursor() 
#         # 如果数据表已经存在使用 execute() 方法删除表。
#         #mycursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
#         # 创建数据表SQL语句

def createDatabase():
    mydb =  mysql.connector.connect(host="localhost",user="root",password="password",database="oneplum",charset="utf8")
    mycursor = mydb.cursor()


    sql = """CREATE TABLE test_one(
        id int (11) PRIMARY KEY  AUTO_INCREMENT,
        date_time char(20) NOT NULL,
        rank_code char(20) NOT NULL)
        ENGINE=InnoDB  DEFAULT CHARSET=utf8"""

    mycursor.execute(sql)
    mycursor.close()



#连接数据库
#获取游标
#插入数据
#发送数据
#关闭数据


def addDatabase(value_date, value_rank):
    mydb =  mysql.connector.connect(host="localhost",user="root",password="password",database="oneplum",charset="utf8")
    mycursor = mydb.cursor()

    sql = "insert into test_one(date_time,rank_code)values('%s','%s')"%(value_date,value_rank)
    try:
        # 执行sql语句
        mycursor.execute(sql)
        # 提交到数据库执行
        mydb.commit()
        print("success")
    except:
         mydb.rollback()
         print("error")
    mycursor.execute(sql)
    mydb.close()



#链接数据库 
#找游标
#写数据库要干嘛、
#try，
#连接游标
#关闭数据库

#删除数据库
def deleteDatabase():
    mydb = mysql.connector.connect(host="192.168.229.136",user="root",password="password",database="oneplum",charset="utf8")
    mycursor = mydb.cursor()

    sql = "delete from test_one where id = 1 "
    try:
        #执行sql语句
        mycursor.execute(sql)
        #提交到数据库执行
        mydb.commit()
        print("success")
    except:
        mydb.rollback()
        print("error")
    #mycursor.execute(sql)
    mydb.close()

#deleteDatabase()


#连接数据库，通过定义一个变量来连接到数据库
#获取数据库游标
#编写数据库要执行的命令
#try
#用获取到的游标q启动数据库
#关闭数据库
import time
def updateDatabase(value3,value4,ids):
    mydb = mysql.connector.connect(host="localhost",user="root",password="password",database="oneplum",charset="utf8")
    mycursor = mydb.cursor()
    # sql = "update test_one set(date_time ,rank_code)values('%s','%s',) "%(value3,value4) where id='%d'%('ids')
    sql = "update test_one set date_time = '%s', rank_code = '%s' where id='%d'"%(value3,value4,ids)
    
    #sql = "UPDATE EMPLOYEE SET AGE = AGE + 1 WHERE SEX = '%c'" % ('M')
    #sql = "insert into test_one(date_time,rank_code)values('%s','%s')"%(value_date,value_rank)

    try:
        #执行sql语句
        mycursor.execute(sql)
        #提交到数据库执行
        mydb.commit()
        print("success!")
    except:
        mydb.rollback()
        print("error")

    #mycursor.execute(sql)
    mydb.close()

value1 = "sadf23"
value2="dshgj"
#addDatabase(value1,value2)


value3="xiaoming"
value4="xiaomei"
id=4
#updateDatabase(value3,value4,id)



#连接数据库
#获取数据库游标
#编写数据
#try
#关闭数据库
def selectDatabase():
    mydb = mysql.connector.connect(host="localhost",user="root",password="password",database="oneplum",charset="utf8")
    mycursor = mydb.cursor()

    sql = "select * from test_one"

    try:
        #执行sql语句
        mycursor.execute(sql)
        #获取所有记录表
        results = mycursor.fetchall()
        #打印结果
        for row in results:
            id = row[0]
            date_time = row[1]
            rank_code = row[2]
            #打印结果
            #print ("id=%d,date_time=%s,rank_code=%s" % (id,date_time,rank_code))               #美观一些
            print(id,date_time,rank_code)
      
        print("success!!!!!!!")
    except:
        mydb.rollback()
        print("error")

    #mycursor.execute(sql)
    mydb.close()

selectDatabase()
ide ="id"
values5 = "date_time"
values6 = "rank_code"
print(ide,values5,values6)





    