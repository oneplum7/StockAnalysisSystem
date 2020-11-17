from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import  QApplication, QHBoxLayout, QWidget, \
     QAction,QMainWindow,QVBoxLayout,QPushButton,QLineEdit,QTextEdit
from PyQt5.QtGui import QIcon
from pyecharts import Bar, Pie, Line, Overlap,Kline
from PyQt5 import QtCore

class Visualization(QMainWindow):
    
    themes = ['light', 'dark']
    themesTip = ['切换为深色主题','切换为浅色主题']

    def __init__(self):
        super().__init__()

        self.BottomView = None
        self.BottomEcharts = False

        self.initUi()
 
    def initUi(self):
    
        self.statusBar().showMessage('加载中...')

        self.setGeometry(100, 100, 600, 1000)
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
        #search_Btn.clicked.connect(self.searchStock)

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
        #h1box.addWidget(RightTableView())
        h1box.addWidget(self.leftTopView)
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

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setStyle('fusion')
    form = Visualization()
    form.show()
    sys.exit(app.exec_())