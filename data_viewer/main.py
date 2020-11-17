# -*- coding: utf-8 -*-
# author:           oneplum7
# create_time:      2020/10
# file_name:        rightview.py
# github           https://github.com/oneplum7?tab=repositories
# qq邮箱            2104878583@qq.com

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import  QApplication, QHBoxLayout, QWidget, \
     QAction,QMainWindow,QVBoxLayout,QPushButton,QLineEdit,QTextEdit
from PyQt5.QtGui import QIcon
from pyecharts import Bar, Pie, Line, Overlap,Kline
from PyQt5 import QtCore
from pyecharts_javascripthon.api import TRANSLATOR
import sys
import qdarkstyle
import myDict
from rightview import RightTableView
import akshare as ak
import pandas as pd
from threading import Timer
import JsCode as Js
import image_rc
from threading import Timer
import mysql.connector

class Visualization(QMainWindow):

    themes = ['light', 'dark']
    themesTip = ['切换为深色主题','切换为浅色主题']

    def __init__(self):
        super().__init__()

        self.BottomView = None
        self.BottomEcharts = False

        self.initUi()

        self.js_init = False

        self.load_html()

        self.leftTopEcharts = False
        
        self.stock_datas = []
        

        self.code = "300750"
        self.findData("300750")
        
        self.upKline()

    def initUi(self):

        self.statusBar().showMessage('加载中...')

        self.setGeometry(100, 60, 600, 400)
        self.setWindowTitle('王梅的股票查询分析系统')
        self.setWindowIcon(QIcon('logo.jpg'))

        self.themeSetAct = QAction('更换图表主题(&T)', self)
        self.themeSetAct.setShortcut('Ctrl+T')
        # 默认浅色主题
        self.themeIndex = 0
        self.themeSetAct.setStatusTip(Visualization.themesTip[self.themeIndex])
        #self.themeSetAct.triggered.connect(self.changeTheme)

        menubar = self.menuBar()
        setMenu = menubar.addMenu('设置(&S)')
        setMenu.addAction(self.themeSetAct)


        self.widget = QWidget()
        self.setCentralWidget(self.widget)

        # 添加web view
        self.leftTopView = QWebEngineView()
        self.leftTopView.setContextMenuPolicy(Qt.NoContextMenu)

        self.BottomView = QWebEngineView()
        self.BottomView.setContextMenuPolicy(Qt.NoContextMenu)

        self.StockLineEdit = QLineEdit(" ")
        search_Btn = QPushButton('搜索')
        search_Btn.clicked.connect(self.searchStock)

        # 搜索布局
        h0box = QHBoxLayout()
        h0box.addWidget(self.StockLineEdit)
        h0box.addWidget(search_Btn)
        h0box.setStretch(0,4)
        h0box.setStretch(1,1)

        # 左上布局
        lefttopbox = QVBoxLayout()
        lefttopbox.addLayout(h0box)
        lefttopbox.addWidget(self.leftTopView)
        lefttopbox.setStretch(0,1)
        lefttopbox.setStretch(1,1)
 
        # 右上布局
        h1box = QHBoxLayout()
        h1box.addLayout(lefttopbox)
        h1box.addWidget(RightTableView())
        #h1box.addWidget(self.leftTopView)
        h1box.setStretch(0,1)
        h1box.setStretch(1,1)

        # 底部布局
        h2box = QHBoxLayout()
        h2box.addWidget(self.BottomView)


        # 整个界面布局
        vbox = QVBoxLayout()
        vbox.addLayout(h1box)
        vbox.addLayout(h2box)
        vbox.setStretch(0,1)
        vbox.setStretch(1,1)


        self.widget.setLayout(vbox)    
    
    def load_html(self):
        self.BottomView.setHtml(Js.html, QtCore.QUrl("index.html"))
        self.BottomView.loadFinished.connect(self.set_options)

    def set_options(self):
        ''' 设置 myChart.setOption 初始化以及各项配置 '''
        if not self.BottomView:    # 如果浏览器对象没有创建
            self.js_init = False    # 将js初始化设置为假
            return  # 并直接返回退出
        
        if not self.js_init:
            # 初始化echarts
            self.BottomView.page().runJavaScript(Js.Pos_Js)       # 执行js页面交互，页面CSS布局和美化
            self.BottomView.page().runJavaScript(Js.splitData)    # 载入K线处理函数
            self.BottomView.page().runJavaScript(Js.echart_init)  # echart 初始化
            self.BottomView.page().runJavaScript(Js.Formula_js)   # 指标
            self.BottomView.page().runJavaScript(
                f'''
                    var KNAME, data, macd;
                    var Zstart = 80;
                    var Zend = 100;
                    var MA1=0, MA2=0, MA3=0, MA4=0, MA5=0, MA6=0;
                    var color1 = "#0CF49B";
                    var color2 = "#FD1050";
                    myChart.clear();
                    var option = eval({Js.Kline_js});
                    myChart.setOption(option);
                '''
            )
            self.BottomView.page().runJavaScript(Js.websize)  # 页面自适应窗体
            self.js_init = True

    def upKline(self, data=None):
        ''' 刷新K线 '''
        if not self.BottomView:    # 如果浏览器对象没有创建
            return  # 并直接返回退出

        kdata = self.stock_datas
        #print(kdata)
        self.BottomView.page().runJavaScript(
            f'''
                KNAME= {self.code};
                data = splitData({kdata});
                macd = MACD(12, 26, 9, data.datas, 1);
                MA1 = MA(20, data.datas, 1);
                MA2 = MA(60, data.datas, 1);
                MA3 = MA(120, data.datas, 1);
                option = eval({Js.Kline_js});
            '''
        )
        self.BottomView.page().runJavaScript(
            '''
                myChart.on('dataZoom',function(event){
                    if(event.batch){
                            Zstart=event.batch[0].start;
                            Zend=event.batch[0].end;
                    }else{
                            Zstart=event.start;
                            Zend=event.end;
                    };
                });

                myChart.setOption(option);

            '''
        )

        sTimer = Timer(10.0, self.upKline, (None,)).start()

    def searchStock(self):
        search_text = self.StockLineEdit.text().strip() # 获取文本框内容并去掉空格

        # 药明康德
        mydb = mysql.connector.connect(host="localhost",user="root",password="gziscas",database="mydatabase",charset='utf8')
        mycursor = mydb.cursor()
        sql = "select * from stock_base \
            where stock_code = '%s' or stock_name = '%s' or short_name = '%s'" % (search_text, search_text, search_text)

        try:
            # 执行sql语句
            mycursor.execute(sql)
            results = mycursor.fetchall()
            if results == None:
                print(results)
            for row in results:
                self.code = row[0]
            # 提交到数据库执行
            mydb.commit()
        except:
            # Rollback in case there is any error
            print("find error.")
            mydb.rollback()
        
        self.findData(self.code)

        mydb.close()

    def addData(self, code, name):
        tmp_stock = ""
        if int(code) > 600000 :
            tmp_stock = "sh" + code
        else:
            tmp_stock = "sz" + code
        stodk_data_daily = ak.stock_zh_a_daily(symbol=tmp_stock, adjust="hfq")
        print(stodk_data_daily)
        mydb = mysql.connector.connect(host="localhost",user="root",password="gziscas",database="mydatabase",charset='utf8')
        mycursor = mydb.cursor() 
        for i in range(0,len(stodk_data_daily)):
            # SQL 插入语句
            data = []
            date=[t.strftime("%Y-%m-%d") for t in stodk_data_daily.index][i]
            open = stodk_data_daily.iat[i,0]
            high = stodk_data_daily.iat[i,1]
            low = stodk_data_daily.iat[i,2]
            close = stodk_data_daily.iat[i,3]
            volume = stodk_data_daily.iat[i,4]
            data.append(date)
            data.append(open)
            data.append(high)
            data.append(low)            
            data.append(close)                      
            data.append(volume)
            self.stock_datas.append(data)   

            # sql = "select * from stock_detail \
            # where code = '%s' and data = '%s'" % (code,date)

            sql = "insert into stock_detail(code, name, date, open, high, low, close, volume) \
                    values('%s','%s','%s','%f','%f','%f','%f','%f')" % \
                   (code, name, date, open, high,low,close,volume)
            try:
                # 执行sql语句
                mycursor.execute(sql)
                # 提交到数据库执行
                mydb.commit()
            except:
                # Rollback in case there is any error
                mydb.rollback()
        mydb.close()

    def findData(self, code):
        mydb = mysql.connector.connect(host="localhost",user="root",password="gziscas",database="mydatabase",charset='utf8')
        mycursor = mydb.cursor() 
        sql = "select * from stock_detail \
            where code = '%s'" % (code)
        try:
        # 执行SQL语句
            mycursor.execute(sql)
            # 获取所有记录列表
            results = mycursor.fetchall()
            if results == None:
                print(results)
            for row in results:
                data = []
                #t.strftime("%Y-%m-%d")
                date = row[3].strftime("%Y-%m-%d")
                open = row[4]
                high = row[5]
                low = row[6]
                close = row[7]
                volume = row[8]
                data.append(date)
                data.append(open)
                data.append(high)
                data.append(low)
                data.append(close)
                data.append(volume)
                self.stock_datas.append(data)
        except:
            print ("find Error: unable to fetch data")

        
        if len(self.stock_datas) == 0:
            self.addData(code, "")

        mydb.close()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    form = Visualization()
    form.show()
    sys.exit(app.exec_())