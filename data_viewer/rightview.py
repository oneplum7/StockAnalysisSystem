# -*- coding: utf-8 -*-
# author:           oneplum7
# create_time:      2020/10
# file_name:        rightview.py
# github           https://github.com/oneplum7?tab=repositories
# qq邮箱            2104878583@qq.com

import akshare as ak
import sys
from PyQt5.QtWidgets import QApplication,QWidget,QVBoxLayout,QTabWidget,QLabel,QTableWidget,QAbstractItemView,QTableWidgetItem
from PyQt5.QtCore import Qt
import mysql.connector
import time
from datetime import datetime


class RightTableView(QWidget):
    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()

        tabWidgets = QTabWidget()

        #label = QLabel("沪股通十大成交股")
        label = QLabel()
        tabWidgets.addTab(label, "沪股通十大成交股")
        #label = QLabel("深股通十大成交股")
        label = QLabel()
        tabWidgets.addTab(label, "深股通十大成交股")

        tabWidgets.currentChanged['int'].connect(self.tabClicked)   # 绑定标签点击时的信号与槽函数

        self.mainLayout.addWidget(tabWidgets)

        self.tableView = QTableWidget()
        self.table = QTableWidget(self)
        self.table.setColumnCount(5)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置表格的选取方式是行选取
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)  # 设置选取方式为单个选取
        self.table.setHorizontalHeaderLabels(["股票代码","股票简称", "收盘价", "当日涨跌幅","净买入","所属版块"])  # 设置行表头

        self.mainLayout.addWidget(self.table)
        self.mainLayout.setStretch(0,1)
        self.mainLayout.setStretch(1,12)
        self.setLayout(self.mainLayout)

        self.hgt = []
        self.sgt = []

        self.stock_em_sgt_hold_stock_df = ak.stock_em_hsgt_hold_stock(market="深股通", indicator="今日排行")
        str_date = self.stock_em_sgt_hold_stock_df.iat[1,1]
        temp = str_date.replace('-','')
        self.table_name = "rank" + temp
        #print(self.table_name)
        if self.checkTableExists(self.table_name) is False:
            self.createDatabase(self.table_name)
            self.addData()

        if len(self.hgt) == 0:
            self.findData()
        

        # 默认显示沪股通
        self.addView()

    def addView(self):
        for i in range(10):
            self.table.insertRow(i)
            # row 0序号 1日期 2 3code 4name 5板块 6板块指数 7 8地理板块 9地理板块指数 
            # 10：150 11 12 13今日收盘价 14今日涨跌幅 15 16今日持股数 17市值 18占流通比 19占总股本比
            # 20：386121563581.44 21 22 23 24今日增持股数 25市值 26市值增幅 27占流通股比 28占总股本比
            stock_code = QTableWidgetItem(self.hgt[i][0])
            stock_code.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
            stock_code.setTextAlignment(Qt.AlignCenter)

            stock_name = QTableWidgetItem(self.hgt[i][1])  # 我们要求它可以修改，所以使用默认的状态即可
            stock_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            stock_name.setTextAlignment(Qt.AlignCenter)

            current_price = QTableWidgetItem(str(self.hgt[i][2]))  # 我们要求它可以修改，所以使用默认的状态即可
            current_price.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            current_price.setTextAlignment(Qt.AlignCenter)


            current_rate = QTableWidgetItem(str(self.hgt[i][3]))  # 我们要求它可以修改，所以使用默认的状态即可
            current_rate.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            current_rate.setTextAlignment(Qt.AlignCenter)


            inflow = QTableWidgetItem(str(self.hgt[i][4]))  # 我们要求它可以修改，所以使用默认的状态即可
            inflow.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            inflow.setTextAlignment(Qt.AlignCenter)


            sction = QTableWidgetItem(self.hgt[i][5])  # 我们要求它可以修改，所以使用默认的状态即可
            sction.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            sction.setTextAlignment(Qt.AlignCenter)


            self.table.setItem(i, 0, stock_code)
            self.table.setItem(i, 1, stock_name)
            self.table.setItem(i, 2, current_price)
            self.table.setItem(i, 3, current_rate)
            self.table.setItem(i, 4, inflow)
            self.table.setItem(i, 5, sction)

    def updateView(self, stock_df):
        self.tableView.clearContents() 
        for i in range(10):
            #self.table.insertRow(i)
            # row 0序号 1日期 2 3code 4name 5板块 6板块指数 7 8地理板块 9地理板块指数 
            # 10：150 11 12 13今日收盘价 14今日涨跌幅 15 16今日持股数 17市值 18占流通比 19占总股本比
            # 20：386121563581.44 21 22 23 24今日增持股数 25市值 26市值增幅 27占流通股比 28占总股本比
            stock_code = QTableWidgetItem(stock_df[i][0])
            stock_code.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择（未设置可编辑）
            stock_code.setTextAlignment(Qt.AlignCenter)

            stock_name = QTableWidgetItem(stock_df[i][1])  # 我们要求它可以修改，所以使用默认的状态即可
            stock_name.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            stock_name.setTextAlignment(Qt.AlignCenter)

            current_price = QTableWidgetItem(str(stock_df[i][2]))  # 我们要求它可以修改，所以使用默认的状态即可
            current_price.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            current_price.setTextAlignment(Qt.AlignCenter)


            current_rate = QTableWidgetItem(str(stock_df[i][3]))  # 我们要求它可以修改，所以使用默认的状态即可
            current_rate.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            current_rate.setTextAlignment(Qt.AlignCenter)


            inflow = QTableWidgetItem(str(stock_df[i][4]))  # 我们要求它可以修改，所以使用默认的状态即可
            inflow.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            inflow.setTextAlignment(Qt.AlignCenter)


            sction = QTableWidgetItem(stock_df[i][5])  # 我们要求它可以修改，所以使用默认的状态即可
            sction.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)  # 设置物件的状态为只可被选择
            sction.setTextAlignment(Qt.AlignCenter)


            self.table.setItem(i, 0, stock_code)
            self.table.setItem(i, 1, stock_name)
            self.table.setItem(i, 2, current_price)
            self.table.setItem(i, 3, current_rate)
            self.table.setItem(i, 4, inflow)
            self.table.setItem(i, 5, sction)
            


    def tabClicked(self,index):
        # 0 沪股通 1 深股通        
        if index == 0:
            self.updateView(self.hgt) 
        elif index == 1:
            self.updateView(self.sgt) 

    def addData(self):        
        self.stock_em_hgt_hold_stock_df = ak.stock_em_hsgt_hold_stock(market="沪股通", indicator="今日排行")

        self.insertData(self.stock_em_hgt_hold_stock_df, 0)
        self.insertData(self.stock_em_sgt_hold_stock_df, 1)

    def findData(self):
        mydb = mysql.connector.connect(host="localhost",user="root",password="gziscas",database="mydatabase",charset='utf8')
        mycursor = mydb.cursor()
        sql = "select * from %s" %(self.table_name)
        try:
        # 执行SQL语句
            mycursor.execute(sql)
            # 获取所有记录列表
            results = mycursor.fetchall()
            print(results)
            if results == None:
                print("111 ", results)
            for row in results:
                data = []
                #t.strftime("%Y-%m-%d")
                flag = row[1]
                stock_code = row[2]
                stock_name = row[3]
                current_price = row[4]
                current_rate = row[5]
                inflow = row[6]
                sction = row[7]
                data.append(stock_code)
                data.append(stock_name)
                data.append(current_price)
                data.append(current_rate)
                data.append(inflow)
                data.append(sction)

                if flag == 0:
                    self.hgt.append(data)
                elif flag == 1:
                    self.sgt.append(data)
        except:
            print ("Error: unable to fetch data")
        mydb.close()

    def insertData(self, stock_df, flag):
        mydb = mysql.connector.connect(host="localhost",user="root",password="gziscas",database="mydatabase",charset='utf8')
        mycursor = mydb.cursor() 

        print(self.table_name)
        for i in range(10):
            # SQL 插入语句
            data = []
            date_time = stock_df.iat[i,1]
            stock_code = stock_df.iat[i,3]
            stock_name = stock_df.iat[i,4]
            current_price = stock_df.iat[i,13]
            current_rate = stock_df.iat[i,14]
            inflow = stock_df.iat[i,17]
            sction = stock_df.iat[i,5]
            data.append(stock_code)
            data.append(stock_name)
            data.append(current_price)
            data.append(current_rate)
            data.append(inflow)
            data.append(sction)
            sql = "insert into %s(date_time,rank_code, stock_code, stock_name, current_price, current_rate, inflow, sction) \
                    values('%s','%d','%s','%s','%f','%f','%f','%s')" % \
                   (self.table_name, date_time,flag, stock_code, stock_name, current_price, current_rate, inflow, sction)
            try:
                # 执行sql语句
                mycursor.execute(sql)
                # 提交到数据库执行
                mydb.commit()

                if flag == 0:
                    self.hgt.append(data)
                elif flag == 1:
                    self.sgt.append(data)
            except:
                mydb.rollback()
        mydb.close()  

    def checkTableExists(self, tablename):
        mydb = mysql.connector.connect(host="localhost",user="root",password="gziscas",database="mydatabase",charset='utf8')
        mycursor = mydb.cursor() 
        mycursor.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(tablename.replace('\'', '\'\'')))
        if mycursor.fetchone()[0] == 1:
            mycursor.close()
            return True

        mycursor.close()
        return False
    
    def createDatabase(self, table_name):
        mydb = mysql.connector.connect(host="localhost",user="root",password="gziscas",database="mydatabase",charset='utf8')
        mycursor = mydb.cursor() 
        # 如果数据表已经存在使用 execute() 方法删除表。
        #mycursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
        # 创建数据表SQL语句
        sql = """CREATE TABLE %s (   
            id int(11) PRIMARY KEY AUTO_INCREMENT,             
            date_time CHAR(20) not null,
            rank_code  INT NOT NULL,
            stock_code  CHAR(20) not null,
            stock_name CHAR(20) not null,  
            current_price float(22,2),
            current_rate float(22,2),
            inflow float(22,2),
            sction CHAR(20))
            ENGINE=InnoDB  DEFAULT CHARSET=utf8"""%(self.table_name)

        mycursor.execute(sql)
        mycursor.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = RightTableView()
    mainWin.show()
    sys.exit(app.exec_())
