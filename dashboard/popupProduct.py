from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QLabel, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

from PyQt5.uic import loadUi
from dashboard.style import Style
from backend.function import *
import json

numbers = 1

class Popup_Product(QMainWindow):
    def __init__(self,shop_choose):
        super(Popup_Product,self,).__init__()
        loadUi("ui//popup_product_push.ui",self)
        self.checkTheme()
        self.resize(1700, 1000)
        self.cc = shop_choose
        self.get_list_products_shopee()

        self.btn_forward.clicked.connect(lambda : self.next_page())
        self.btn_back.clicked.connect(lambda : self.back_page())

        self.btn_confirm.clicked.connect(lambda : self.add_to_product_push())
        self.btn_cancel.clicked.connect(lambda : self.close())

        self.btnSearch.clicked.connect(lambda: self.searchProduct())
        self.searchLineEdit.returnPressed.connect(lambda: self.searchProduct())

    def searchProduct(self):
        search = self.searchLineEdit.text()
        for i in reversed(range(self.tableWidget_product_push_shopee.rowCount())):
            self.tableWidget_product_push_shopee.removeRow(i)
        if search != "":
            self.get_list_products_shopee(self.searchLineEdit.text())           
        elif search == "":
            self.get_list_products_shopee()

    def get_list_products_shopee(self,keyword=""):      
        self.tableWidget_product_push_shopee.setRowCount(24)
        for k in range(self.tableWidget_product_push_shopee.rowCount()):
            self.tableWidget_product_push_shopee.setRowHeight(k, 90)
        self.tableWidget_product_push_shopee.setColumnWidth(0, 50)
        self.tableWidget_product_push_shopee.setColumnWidth(1, 100)
        self.tableWidget_product_push_shopee.setColumnWidth(2, 700)
        self.tableWidget_product_push_shopee.setColumnWidth(3, 140)
        self.tableWidget_product_push_shopee.setColumnWidth(4, 140)
        self.tableWidget_product_push_shopee.setColumnWidth(5, 140)
        self.tableWidget_product_push_shopee.setColumnWidth(6, 140)
        self.tableWidget_product_push_shopee.setItem(0, 2,QTableWidgetItem("Đang tải dữ liệu ...."))      
        global numbers  
        with open('temp//data.json') as f:
            data = json.load(f)
            self.id_wp = data['id_wp']          
            if len(data['shopee']) != 0:
                c = data['shopee'][self.cc]['cookie']             
                self.worker_product = ThreadGetListProduct(c,numbers,keyword)
                self.worker_product.start()
                self.worker_product.r_json.connect(self.update_list_products_shopee)
    
    def update_list_products_shopee(self, l):
        self.r = l[0]
        self.page_number = l[1]
        self.checkTheme()
        a = self.r['data']['page_info']['total']

        page_size = 1 if a <= 24 else (a // 24) +1
        self.btn_back.setEnabled(False) if self.page_number == 1 else self.btn_back.setEnabled(True)
        self.btn_forward.setEnabled(False) if self.page_number == page_size else self.btn_forward.setEnabled(True)

        if len(self.r['data']['list']) != 0:
            self.name = []
            self.img = []  
            self.ids = []  
            self.stock = []       
            self.normal_price = []
            self.promotion_price = []
            self.sold = []
            self.parent_sku = []
            for x in range(len(self.r['data']['list'])):
                self.name.append(self.r['data']['list'][x]['name'])
                self.img.append(self.r['data']['list'][x]['images'][0])
                self.ids.append(self.r['data']['list'][x]['id'])
                self.stock.append(self.r['data']['list'][x]['stock'])
                self.normal_price.append(self.r['data']['list'][x]['price_info']['normal_price'])
                self.promotion_price.append(self.r['data']['list'][x]['price_info']['promotion_price'])
                self.sold.append(self.r['data']['list'][x]['sold'])
                self.parent_sku.append(self.r['data']['list'][x]['parent_sku'])
            for row ,data_name in enumerate(self.name):                
                self.tableWidget_product_push_shopee.setItem(row, 2,QTableWidgetItem(data_name))

            for row ,parent_sku in enumerate(self.parent_sku):                
                self.tableWidget_product_push_shopee.setItem(row, 3,QTableWidgetItem(parent_sku))

            for row ,stock in enumerate(self.stock):                
                self.tableWidget_product_push_shopee.setItem(row, 4,QTableWidgetItem(str(stock)))

            for row ,normal_price in enumerate(self.normal_price):                
                self.tableWidget_product_push_shopee.setItem(row, 5,QTableWidgetItem(normal_price))

            for row ,promotion_price in enumerate(self.promotion_price):                
                self.tableWidget_product_push_shopee.setItem(row, 6,QTableWidgetItem(promotion_price))

            for row ,sold in enumerate(self.sold):                
                self.tableWidget_product_push_shopee.setItem(row, 7,QTableWidgetItem(str(sold)))

            self.workerthread = WorkerThread(self.img,'product_list_shopee')
            self.workerthread.start()
            self.workerthread.img_complete.connect(self.update_img)

    def update_img(self,l):
        i = QImage()
        i.loadFromData(l[1]) 
        imgLabel = QLabel()
        imgLabel.setText('')
        imgLabel.setScaledContents(True)    
        imgLabel.setPixmap(QPixmap(i))

        self.tableWidget_product_push_shopee.setCellWidget(l[0],1,imgLabel)

    def next_page(self):
        global numbers
        numbers += 1
        for i in reversed(range(self.tableWidget_product_push_shopee.rowCount())):
            self.tableWidget_product_push_shopee.removeRow(i) 
        self.get_list_products_shopee()

    def back_page(self):
        global numbers
        if numbers <= 1:
            numbers = 1
        elif numbers > 1:
            numbers -= 1
            for i in reversed(range(self.tableWidget_product_push_shopee.rowCount())):
                self.tableWidget_product_push_shopee.removeRow(i) 
            self.get_list_products_shopee()

    def add_to_product_push(self):
        x = self.tableWidget_product_push_shopee.selectedItems()
        l = []
        data = []
        for i in x:
            l.append(i.row())
        for p in set(l):
            k ={}
            k['image'] = self.img[p]
            k['name'] = self.name[p]
            k['ids'] = self.ids[p]
            k['stock'] = self.stock[p] 
            k['parent_sku'] = self.parent_sku[p]
            k['normal_price'] = self.normal_price[p]
            k['promotion_price'] = self.promotion_price[p]
            k['sold'] = self.sold[p]
            k['done'] = 'False'
            data.append(k)
        r , change = Database_mongoDB.add_protuct_push(self,self.id_wp,self.cc,data)

        if r['updatedExisting'] == True:
            self.tableWidget_product_push_shopee.clearSelection()
            duplicate = len(set(l)) - change
            if duplicate == 0 :
                self.showPopup("Thành Công","Thêm sản phẩm thành công",f"{change} sản phẩm được chọn đã thêm thành công",True)
            else:
                self.showPopup("Thành Công","Thêm sản phẩm thành công",f"{change} sản phẩm thêm thành công và {duplicate} sản phẩm bị trùng ",True)    
        else:
            self.showPopup("Không Thành Công","Thêm sản phẩm không thành công","Vui lòng liên hệ fanpage để được trợ giúp",False)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


    def showPopup(self,title,info,notification,c=True):   
        msg = QMessageBox()   
        msg.setWindowTitle(title)
        msg.setText(notification)
        msg.setInformativeText(info)
        if c == True:
            msg.setIconPixmap(QPixmap("img//success.png"))
        else:
            msg.setIconPixmap(QPixmap("img//warning.png"))
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def checkTheme(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        if data['theme'] == 'dark':
            self.centralwidget.setStyleSheet(Style.productPush_dark)
        elif data['theme'] == 'light':
            self.centralwidget.setStyleSheet(Style.productPush_light)