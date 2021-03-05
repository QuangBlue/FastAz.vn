from main_pyqt5 import *
from dashboard.dashboard import *
from backend.function import *

class UserShopee:

    def openBrowserAddUserShopee(self):
        profileShopee = r = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for i in range(8))
        self.ui = Browser(profileShopee)
        self.ui.show()
        self.ui.msg.buttonClicked.connect(lambda: UserShopee.setDataUserShopee(self))
        self.ui.msg.buttonClicked.connect(lambda: UserShopee.setComboBoxUser(self))
        self.ui.msg.buttonClicked.connect(lambda: self.ui.close())
        UIFunctions.writeLog(self,f'Tạo profile {profileShopee}')

    def setDataUserShopee(self):
        with open('temp//data.json') as f:
            data = json.load(f)
            shopee = data['shopee']
        row = 0
        self.tableWidget.setRowCount(len(shopee) if len(shopee) >25 else 25)

        self.tableWidget.setColumnWidth(0, 70)
        self.tableWidget.setColumnWidth(1, 180)
        self.tableWidget.setColumnWidth(2, 280)
        self.tableWidget.setColumnWidth(3, 180)
        self.tableWidget.setColumnWidth(4, 200)
        self.tableWidget.setColumnWidth(5, 200)

        if len(shopee) != 0:            
            for data in shopee:
                self.btn_del_user = QPushButton('')
                self.btn_del_user.clicked.connect(lambda: UserShopee.btnDelUser(self))
                self.tableWidget.setCellWidget(row,0,self.btn_del_user)
                self.btn_del_user.setStyleSheet('QPushButton { image: url(img//remove.png);background: transparent;}QPushButton:hover { image: url(img//remove_red.png);}')
                self.tableWidget.setItem(row, 1,QTableWidgetItem(data['id_sp']))
                self.tableWidget.setItem(row, 2,QTableWidgetItem(data['shop_name']))
                self.tableWidget.setItem(row, 3,QTableWidgetItem(data['shop_id']))
                self.tableWidget.setItem(row, 4,QTableWidgetItem(data['total_product']))
                self.tableWidget.setItem(row, 5,QTableWidgetItem(data['total_order']))
                UIFunctions.writeLog(self,f'Hiển thị thông tin User Shopee {data["shop_name"]}')
                if data['status_cookie'] == 'True':
                    layout = QHBoxLayout()
                    label = QLabel('Còn Hiệu Lực')
                    font = QFont()
                    font.setBold(True)
                    font.setFamily(u"Nunito")
                    font.setPointSize(16)
                    label.setStyleSheet(u"color: rgb(73, 165, 43);")
                    label.setMaximumSize(QSize(110, 16777215))
                    label.setFont(font)
                    layout.addWidget(label)
                    layout.setContentsMargins(10, 0, 0, 0)
                    cellWidget = QWidget()
                    cellWidget.setLayout(layout)                   
                    self.tableWidget.setCellWidget(row, 6, cellWidget)               

                else:
                    layout = QHBoxLayout()
                    label = QLabel('Hết Hiệu Lực')
                    font = QFont()
                    font.setBold(True)
                    font.setFamily(u"Nunito")
                    font.setPointSize(16)
                    label.setStyleSheet(u"color: rgb(201, 5, 22);")
                    label.setMaximumSize(QSize(110, 16777215))
                    label.setMinimumSize(QSize(110, 0))
                    label.setFont(font)
                    btn_gh = QPushButton('Gia Hạn')
                    btn_gh.setFont(font)
                    btn_gh.setMinimumSize(QSize(100, 0))
                    btn_gh.setMaximumSize(QSize(100, 16777215))
                    btn_gh.setStyleSheet("QPushButton { border-radius: 10px; background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(89, 64, 231, 255), stop:1 rgba(15, 181, 253, 255));color: rgb(255, 255, 255);} QPushButton:hover { background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(15, 181, 253, 255), stop:1 rgba(89, 64, 231, 255));}QPushButton:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(89, 64, 231, 255), stop:1 rgba(15, 181, 253, 255));}")
                    btn_gh.clicked.connect(lambda: UserShopee.openBrowserAddUserShopee(self))
                    
                    f = QFrame()
                    f1 = QFrame()
                    layout.addWidget(f1)
                    layout.addWidget(label)
                    layout.addWidget(btn_gh)
                    layout.addWidget(f)
                    layout.setContentsMargins(0, 0, 0, 0)
                    cellWidget = QWidget()
                    cellWidget.setLayout(layout)                   
                    self.tableWidget.setCellWidget(row, 6, cellWidget)                             
                row = row + 1
                
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.setRowHeight(row, 50)
    def setComboBoxUser(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        self.comboBox_user.clear()   
        l = []
        if len(data['shopee']) != 0 :
            for x in range(len(data['shopee'])):
                if data['shopee'][x]['status_cookie'] == "True":
                    # self.comboBox_user.addItem(data['shopee'][x]['shop_name'])
                    l.append(data['shopee'][x]['shop_name'])
            if len(l) > 0:
                self.comboBox_user.addItems(l)    


    def btnDelUser(self):
        x = QMessageBox.warning(self, 'MessageBox', "TẤT CẢ DỮ LIỆU SẼ MẤT \nBạn có chắc chắn muốn xóa tài khoản này không ?", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if x == QMessageBox.Yes:
            button = self.sender()
            index = self.tableWidget.indexAt(button.pos())
            with open('temp//data.json') as f:
                data = json.load(f)


            Database_mongoDB.registered_Users_Collection.update({"_id": data['id_wp']}, {"$unset": {f"shopee.{index.row()}": 1}})
            Database_mongoDB.registered_Users_Collection.update({"_id": data['id_wp']}, {"$pull": {"shopee": None}})

            try:
                ind = self.comboBox_user.findText(data['shopee'][index.row()]['shop_name'])
                self.comboBox_user.removeItem(ind)
            except:
                pass

            del data['shopee'][index.row()]
            with open('temp//data.json', 'w') as f:
                json.dump(data, f)

            for i in reversed(range(self.tableWidget.rowCount())):
                self.tableWidget.removeRow(i)  
                


            UIFunctions.writeLog(self,'Xóa tài khoản Shopee')       
            UserShopee.setDataUserShopee(self)
