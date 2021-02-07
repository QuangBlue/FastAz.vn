from main_pyqt5 import *
from dashboard.s_db import *
from dashboard.browser import Browser
from data_example import *
from backend.MongoDB_Setup import * 

shop_choose = 0

class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard,self).__init__()
        loadUi("ui//dashboard_screen.ui",self)
        self.resize(1920, 1080)
        QtGui.QFontDatabase.addApplicationFont('font/Nunito/Nunito-Regular.ttf')
        QtGui.QFontDatabase.addApplicationFont('font/Nunito/Nunito-Regular.ttf')
        # ########################################################################
        ## THÊM NUT MENU TẠI ĐÂY
        # ########################################################################
        #
        # B1: Tạo function thêm nút ---> addNewMenu(self, name, objName, icon, isTopMenu):
        # B2: Thêm nút Menu vào def Button
        self.stackedWidget.setMinimumWidth(20)
        UIFunctions.addNewMenu(self, "Tài khoản Shopee", "btn_new_user_shopee", "url(:/icon/cil-user-follow.png)", True)
        UIFunctions.addNewMenu(self, "Trả lời Đánh giá", "btn_reply_ratting", "url(:/icon/cil-star.png)", True)
        UIFunctions.addNewMenu(self, "Đẩy sản phẩm", "btn_push_product", "url(:/icon/cil-chevron-double-up-alt.png)", True)
        UIFunctions.addNewMenu(self, "Chat bot", "btn_chat_bot", "url(:/icon/cil-mood-very-good.png)", True)
        UIFunctions.addNewMenu(self, "Setting", "btn_settings", "url(:/icon/cil-settings.png)", False)


        # ########################################################################
        ## HIỂN THỊ SHOPEE
        # ########################################################################

        self.set_data_user_shopee()
        self.set_data_rating_shopee()
        self.comboBox_user.currentTextChanged.connect(self.set_data_rating_shopee)
        self.btn_add_rating.clicked.connect(self.pop_up_rating)
        self.btn_apply_all_rating.clicked.connect(self.set_data_rating_shopee)


        # ########################################################################
        ## ICON HOẶC AVARTA CỦA USER
        # ########################################################################

        UIFunctions.userIcon(self, "QH")
        self.label_user_icon.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.label_user_icon.mousePressEvent = self.show_popup_user
        # self.label_user_icon.customContextMenuRequested.connect(lambda pos, child=self.label_user_icon: self.customMenuEvent(pos, child))
        # ########################################################################
        ## ẨN CỬA SỔ MẶC ĐỊNH
        # ########################################################################
        UIFunctions.removeTitleBar(self,True)

        # ########################################################################
        ## THIỆT LẬP TÊN CỬA SỔ VÀ THÔNG TIN THÔNG BÁO
        # ########################################################################
        self.setWindowTitle('FastAz.vn - Ứng dụng bán hàng chuyên nghiệp')
        UIFunctions.labelTitle(self, 'FastAz.vn - Ứng dụng bán hàng chuyên nghiệp')
        UIFunctions.labelDescription(self, 'Mọi câu hỏi hoặc khó khăn vui lòng liên hệ Fanpage FastAz.Vn - Ứng dụng hỗ trợ bán hàng chuyên nghiệp')

        # ########################################################################
        ## DI CHUYỂN CỬA SỔ
        # ########################################################################
        def moveWindow(event):
            if self.isMaximized() == False:
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()
        self.frame_label_top_btns.mouseMoveEvent = moveWindow

        # ########################################################################
        ## NÚT TOGGLE
        # ########################################################################
        self.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))

        
        # ########################################################################
        ## NÚT MỞ BROWER --> ADD USER SHOPEE
        # ########################################################################

        self.btn_add_user.clicked.connect(lambda: UIFunctions.open_browser(self))

        # ########################################################################
        ## LỰA CHỌN MENU MẶC ĐỊNH
        # ########################################################################
        
        UIFunctions.selectStandardMenu(self, "btn_new_user_shopee")
        self.stackedWidget.setCurrentWidget(self.page_new_user_shopee)

        # ########################################################################
        ## HÀM CHẠY CÁC CHỨC NĂNG CỦA CỬA SỔ
        # ########################################################################
        UIFunctions.uiDefinitions(self)
        self.show()
    def set_data_rating_shopee(self):
        with open('temp//data.json') as f:
            data = json.load(f)
            shopee = data['shopee']
        shop_c = 0
        for x in range(len(data['shopee'])):
                if data['shopee'][x]['shop_name'] == self.comboBox_user.currentText():
                    shop_c = x           
        s1 = data['shopee'][shop_c]['reply_rating']['rating_1star']
        s2 = data['shopee'][shop_c]['reply_rating']['rating_2star']
        s3 = data['shopee'][shop_c]['reply_rating']['rating_3star']
        s4 = data['shopee'][shop_c]['reply_rating']['rating_4star']
        s5 = data['shopee'][shop_c]['reply_rating']['rating_5star']
        self.tw_ratting1.setRowCount(len(s1))
        self.tw_ratting2.setRowCount(len(s2))
        self.tw_ratting3.setRowCount(len(s3))
        self.tw_ratting4.setRowCount(len(s4))
        self.tw_ratting5.setRowCount(len(s5))
  
        row = 0
        for data in s1:                   
            self.tw_ratting1.setItem(row, 1,QtWidgets.QTableWidgetItem(str(row+1)))
            self.tw_ratting1.setItem(row, 2,QtWidgets.QTableWidgetItem(data))
            self.btn_delete1 = QPushButton('')
            self.btn_delete1.clicked.connect(self.delete1)
            self.tw_ratting1.setCellWidget(row,0,self.btn_delete1)
            self.btn_delete1.setStyleSheet('QPushButton { image: url(img//remove.png);}QPushButton:hover { image: url(img//remove_red.png);}')
            row = row + 1
        row = 0
        for data_2 in s2:                   
            self.tw_ratting2.setItem(row, 1,QtWidgets.QTableWidgetItem(str(row+1)))
            self.tw_ratting2.setItem(row, 2,QtWidgets.QTableWidgetItem(data_2))
            self.btn_delete2 = QPushButton('')
            self.btn_delete2.clicked.connect(self.delete2)
            self.tw_ratting2.setCellWidget(row,0,self.btn_delete2)
            self.btn_delete2.setStyleSheet('QPushButton { image: url(img//remove.png);}QPushButton:hover { image: url(img//remove_red.png);}')          
            row = row + 1
        row = 0
        for data_3 in s3:                   
            self.tw_ratting3.setItem(row, 1,QtWidgets.QTableWidgetItem(str(row+1)))
            self.tw_ratting3.setItem(row, 2,QtWidgets.QTableWidgetItem(data_3))
            self.btn_delete3 = QPushButton('')
            self.btn_delete3.clicked.connect(self.delete3)
            self.tw_ratting3.setCellWidget(row,0,self.btn_delete3)
            self.btn_delete3.setStyleSheet('QPushButton { image: url(img//remove.png);}QPushButton:hover { image: url(img//remove_red.png);}')
            row = row + 1
        row = 0
        for data_4 in s4:                   
            self.tw_ratting4.setItem(row, 1,QtWidgets.QTableWidgetItem(str(row+1)))
            self.tw_ratting4.setItem(row, 2,QtWidgets.QTableWidgetItem(data_4))
            self.btn_delete4 = QPushButton('')
            self.btn_delete4.clicked.connect(self.delete4)
            self.tw_ratting4.setCellWidget(row,0,self.btn_delete4)
            self.btn_delete4.setStyleSheet('QPushButton { image: url(img//remove.png);}QPushButton:hover { image: url(img//remove_red.png);}')
            row = row + 1
        row = 0
        for data_5 in s5:                   
            self.tw_ratting5.setItem(row, 1,QtWidgets.QTableWidgetItem(str(row+1)))
            self.tw_ratting5.setItem(row, 2,QtWidgets.QTableWidgetItem(data_5))
            self.btn_delete5 = QPushButton('')
            self.btn_delete5.clicked.connect(self.delete5)
            self.tw_ratting5.setCellWidget(row,0,self.btn_delete5)
            self.btn_delete5.setStyleSheet('QPushButton { image: url(img//remove.png);}QPushButton:hover { image: url(img//remove_red.png);}')
            row = row + 1   

        QTimer.singleShot(500,self.set_data_rating_shopee)
    def set_data_user_shopee(self):
        with open('temp//data.json') as f:
            data = json.load(f)
            shopee = data['shopee']
        row = 0
        self.tableWidget.setRowCount(len(shopee) if len(shopee) >25 else 25)
        for data in shopee:
            self.tableWidget.setItem(row, 0,QtWidgets.QTableWidgetItem(data['id_sp']))
            self.tableWidget.setItem(row, 1,QtWidgets.QTableWidgetItem(data['shop_name']))
            self.tableWidget.setItem(row, 2,QtWidgets.QTableWidgetItem(data['shop_id']))
            self.tableWidget.setItem(row, 3,QtWidgets.QTableWidgetItem(data['total_product']))
            self.tableWidget.setItem(row, 4,QtWidgets.QTableWidgetItem(data['total_order']))
            self.tableWidget.setItem(row, 5,QtWidgets.QTableWidgetItem('Còn Hiệu Lực') if data['status_cookie'] == 'True' else QtWidgets.QTableWidgetItem('Hết Hiệu Lực'))
            self.tableWidget.item(row, 5).setForeground(QtGui.QColor(73, 165, 43) if data['status_cookie'] == 'True' else QtGui.QColor(201, 5, 22))
            font = QtGui.QFont()
            font.setBold(True)
            self.tableWidget.item(row, 5).setFont(font)
            row = row + 1
        if len(shopee) > 0:
            self.comboBox_user.removeItem(0)
            for x in range(len(shopee)):
                self.comboBox_user.addItem(shopee[x]['shop_name'])

        self.comboBox_user.currentTextChanged.connect(lambda: print(self.comboBox_user.currentText()))

        Dashboard.comboBox_user_text = self.comboBox_user.currentText()

    def pop_up_rating(self):
        self.ui = Popup_Rating()
        self.ui.show()

    def delete1(self):
        self.pos_table = self.tw_ratting1
        self.table_name = 'rating_1star'
        self.delete_ratings()

    def delete2(self):
        self.pos_table = self.tw_ratting2
        self.table_name = 'rating_2star'
        self.delete_ratings()

    def delete3(self):
        self.pos_table = self.tw_ratting3
        self.table_name = 'rating_3star'
        self.delete_ratings()        

    def delete4(self):
        self.pos_table = self.tw_ratting4
        self.table_name = 'rating_4star'
        self.delete_ratings()

    def delete5(self):
        self.pos_table = self.tw_ratting5
        self.table_name = 'rating_5star'
        self.delete_ratings()

    def delete_ratings(self):
        button = self.sender()
        index = self.pos_table.indexAt(button.pos())

        with open('temp//data.json') as f:
            data = json.load(f)
            shopee = data['shopee']
        shop_c = 0
        for x in range(len(data['shopee'])):
                if data['shopee'][x]['shop_name'] == self.comboBox_user.currentText():
                    shop_c = x  
        k = data['shopee'][shop_c]['reply_rating'][self.table_name][index.row()]
        del data['shopee'][shop_c]['reply_rating'][self.table_name][index.row()]
        with open('temp//data.json', 'w') as f:
            json.dump(data, f)
        Database_mongoDB.registered_Users_Collection.update_one(
            { '_id': data['id_wp'] },
            { '$pull': { f'shopee.{shop_c}.reply_rating.{self.table_name}': k } }
            )
        
    def show_popup_user(self,event):
        msg = QMessageBox()
        msg.setWindowTitle('Thông tin tài khoản')
        msg.setText('Tài khoản của bạn là <strong>VIP 1</strong> \n Còn thời hạn đến 16/03/2022')
        logout_btn = msg.addButton('Đăng Xuất' , QtWidgets.QMessageBox.RejectRole)
        logout_btn.clicked.connect(self.logout_screen)
        extend_vip = msg.addButton('Gia Hạn' , QtWidgets.QMessageBox.YesRole)
        extend_vip.clicked.connect(self.open_webbrowser)
        msg.exec_()
        
    def logout_screen(self):
        # f = open("temp//data.json", "w")
        # data = json.load(f)
        # data['savepass'] = "False"
        # json.dump(data,f)
        # f.close()
        with open('temp//data.json') as f:
            data = json.load(f)
        data['savepass'] = "False"
        with open('temp//data.json', 'w') as f:
            json.dump(data, f)
        MainWindow()
        self.close()

    def open_webbrowser(self):
        webbrowser.open('http://fastaz.vn/')


    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def resizeEvent(self, event):
        return super(Dashboard, self).resizeEvent(event)

    def Button(self):
        btnWidget = self.sender()

        if btnWidget.objectName() == "btn_new_user_shopee":
            self.stackedWidget.setCurrentWidget(self.page_new_user_shopee)
            UIFunctions.resetStyle(self, "btn_new_user_shopee")
            UIFunctions.labelPage(self, "Tài khoản Shopee")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_reply_ratting":
            self.stackedWidget.setCurrentWidget(self.page_reply_ratting)
            UIFunctions.resetStyle(self, "btn_reply_ratting")
            UIFunctions.labelPage(self, "Trả lời Đánh giá")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self, btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_push_product":
            self.stackedWidget.setCurrentWidget(self.page_push_product)
            UIFunctions.resetStyle(self, "btn_push_product")
            UIFunctions.labelPage(self, "Đẩy sản phẩm")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_chat_bot":
            self.stackedWidget.setCurrentWidget(self.page_chat_bot)
            UIFunctions.resetStyle(self, "btn_chat_bot")
            UIFunctions.labelPage(self, "Chat bot")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_settings":
            self.stackedWidget.setCurrentWidget(self.page_settings)
            UIFunctions.resetStyle(self, "btn_settings")
            UIFunctions.labelPage(self, "Setting")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))


class Popup_Rating(QMainWindow):
    def __init__(self):
        super(Popup_Rating,self).__init__()
        loadUi("ui//popup_ratting.ui",self)

        self.btn_send.clicked.connect(self.send_info_ratting)

        self.dashboard_screen = Dashboard()
        self.dashboard_screen.close()

    def send_info_ratting(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        id_db = data['id_wp']
        new_rating = self.plainTextEdit_ratting.toPlainText().replace("\n",". ")
        if self.comboBox_ratting.currentText() == "Đánh giá 1 sao":
            select = 'rating_1star'
            table = 'tw_ratting1'
            delete_bt = self.dashboard_screen.delete1
        elif self.comboBox_ratting.currentText() == "Đánh giá 2 sao":
            select = 'rating_2star'
            table = 'tw_ratting2'
            delete_bt = self.dashboard_screen.delete2      
        elif self.comboBox_ratting.currentText() == "Đánh giá 3 sao":
            select = 'rating_3star'
            table = 'tw_ratting3'
            delete_bt = self.dashboard_screen.delete3
        elif self.comboBox_ratting.currentText() == "Đánh giá 4 sao":
            select = 'rating_4star'
            table = 'tw_ratting4'
            delete_bt = self.dashboard_screen.delete4     
        elif self.comboBox_ratting.currentText() == "Đánh giá 5 sao":
            select = 'rating_5star'
            table = 'tw_ratting5'
            delete_bt = self.dashboard_screen.delete5


        if len(new_rating) > 10 and len(new_rating) < 500 :
            for x in range(len(data['shopee'])):
                if data['shopee'][x]['shop_name'] == Dashboard.comboBox_user_text:
                    k = Database_mongoDB.registered_Users_Collection.find_one({'_id':id_db})
                    k['shopee'][x]['reply_rating'][select].append(new_rating)
                    data['shopee'][x]['reply_rating'][select].append(new_rating)
                    with open('temp//data.json', 'w') as f:
                        json.dump(data, f)
                    Database_mongoDB.registered_Users_Collection.replace_one({'_id':id_db},k,upsert = True)
                    self.show_popup('Thành công',f'Đã thêm thành công nội dụng trả lời cho {self.comboBox_ratting.currentText()}')
                    self.close()
        else:
            self.show_popup('Lỗi', 'Câu trả lời phải hơn 10 ký tự và nhỏ hơn 500 ký tự')


    def show_popup(self,title,notification):
        msg = QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(notification)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

