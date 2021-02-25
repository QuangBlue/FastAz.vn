from dashboard.dashboard import *
from dashboard.browser import Browser
from backend.MongoDB_Setup import Database_mongoDB

GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True

count = 1
page_number = 1
shop_choose = 0
theme_style = 'dark'
class UIFunctions:
    GLOBAL_STATE = 0
    GLOBAL_TITLE_BAR = True

    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == 0:
            self.showMaximized()
            GLOBAL_STATE = 1
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.btn_maximize_restore.setToolTip("Restore")
            self.btn_maximize_restore.setIcon(QIcon(u":/icon/cil-window-restore.png"))
            self.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.btn_maximize_restore.setToolTip("Maximize")
            self.btn_maximize_restore.setIcon(QIcon(u":/icon/cil-window-maximize.png"))
            self.frame_size_grip.show()

    def removeTitleBar(self, status):
        global GLOBAL_TITLE_BAR
        GLOBAL_TITLE_BAR = status

    def labelTitle(self, text):
        self.label_title_bar_top.setText(text)

    # LABEL DESCRIPTION
    def labelDescription(self, text):
        self.label_top_info_1.setText(text)

    def toggleMenu(self, maxWidth, enable):
        if enable:
            width = self.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 75

            if width == 75:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            self.animation = QPropertyAnimation(self.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(300)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    def addNewMenu(self, name, objName, icon, isTopMenu):
        font = QFont()
        font.setFamily(u"Nunito")
        font.setPointSize(16)
        self.button = QPushButton(str(count),self)
        self.button.setObjectName(objName)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.button.sizePolicy().hasHeightForWidth())
        self.button.setSizePolicy(sizePolicy3)
        self.button.setMinimumSize(QSize(0, 75))
        self.button.setLayoutDirection(Qt.LeftToRight)
        self.button.setFont(font)
        try:
            with open('temp//data.json') as f:
                data = json.load(f)
            if data['theme'] == 'light':
                self.button.setStyleSheet(Style.style_bt_light.replace('ICON_REPLACE', icon))
            else:
                self.button.setStyleSheet(Style.style_bt_dark.replace('ICON_REPLACE', icon))    
        except:
            self.button.setStyleSheet(Style.style_bt_dark.replace('ICON_REPLACE', icon))    
        self.button.setText(name)
        self.button.setToolTip(name)
        self.button.clicked.connect(self.Button)

        if isTopMenu:
            self.layout_menus.addWidget(self.button)
        else:
            self.layout_menu_bottom.addWidget(self.button)

    def selectMenu(self, getStyle):
        select = getStyle + ("QPushButton { border-right: 7px solid rgb(85, 170, 255); }")
        return select

    def deselectMenu(self, getStyle):
        deselect = getStyle.replace("QPushButton { border-right: 7px solid rgb(85, 170, 255); }", "")
        return deselect

    def selectStandardMenu(self, widget):
        for w in self.frame_left_menu.findChildren(QPushButton):
            if w.objectName() == widget:
                w.setStyleSheet(UIFunctions.selectMenu(self,w.styleSheet()))

    def resetStyle(self, widget):
        for w in self.frame_left_menu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(self,w.styleSheet()))

    def labelPage(self, text):
        newText = '| ' + text.upper()
        self.label_top_info_2.setText(newText)

    def open_browser(self):
        self.ui = Browser()
        self.ui.show()
        self.ui.msg.buttonClicked.connect(lambda: UIFunctions.set_data_user_shopee(self))
        self.ui.msg.buttonClicked.connect(lambda: UIFunctions.set_comboBox_user(self))
        self.ui.msg.buttonClicked.connect(lambda: self.ui.close())
        self.ui.msg.buttonClicked.connect(lambda: QTimer.singleShot(10, lambda: UIFunctions.get_list_products_shopee(self)))

        
    def userIcon(self, icon = 'img//teamwork.png'):
        self.label_user_icon.setIcon(QIcon(icon))
        self.label_user_icon.setIconSize(QSize(60,60))

        self.label_user_icon.clicked.connect(lambda: UIFunctions.show_popup_user(self))

    def show_popup_user(self):
        msg = QMessageBox()
        msg.setWindowTitle('Thông tin tài khoản')
        msg.setText('Tài khoản của bạn là <strong>VIP 1</strong> \n Còn thời hạn đến 16/03/2022')
        logout_btn = msg.addButton('Đăng Xuất' , QMessageBox.RejectRole)
        logout_btn.clicked.connect(lambda: UIFunctions.logout_screen(self))
        extend_vip = msg.addButton('Gia Hạn' , QMessageBox.YesRole)
        extend_vip.clicked.connect(lambda: UIFunctions.open_webbrowser(self))
        msg.exec_()
        
    def logout_screen(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        data['savepass'] = "False"
        with open('temp//data.json', 'w') as f:
            json.dump(data, f)
        MainWindow()
        self.close()

    def open_webbrowser(self):
        webbrowser.open('http://fastaz.vn/')
    
    def check_shop_choose(self):
        global shop_choose
        if self.comboBox_user.currentText() != 'Chưa có tài khoản':
            with open('temp//data.json') as f:
                data = json.load(f)
            for x in range(len(data['shopee'])):
                if data['shopee'][x]['shop_name'] == self.comboBox_user.currentText():
                    shop_choose = x

    def get_list_products_shopee(self):
        self.product_list_shopee.setRowCount(24)
        for k in range(self.product_list_shopee.rowCount()):
            self.product_list_shopee.setRowHeight(k, 90)
        self.product_list_shopee.setItem(0, 1,QTableWidgetItem("Đang tải dữ liệu ...."))
        if self.comboBox_user.currentText() != 'Chưa có tài khoản':
            global page_number
            with open('temp//data.json') as f:
                data = json.load(f)
                self.id_wp = data['id_wp']
            
            if len(data['shopee']) != 0:
                UIFunctions.check_shop_choose(self)
                c = data['shopee'][shop_choose]['cookie']
                self.worker_product = ThreadGetListProduct(c,page_number)
                self.worker_product.start()
                self.worker_product.r_json.connect(self.update_list_products_shopee)

    def next_page(self):
        global page_number
        page_number += 1
        for i in reversed(range(self.product_list_shopee.rowCount())):
            self.product_list_shopee.removeRow(i) 
        UIFunctions.get_list_products_shopee(self)

    def back_page(self):
        global page_number
        if page_number <= 1:
            page_number = 1
        elif page_number > 1:
            page_number -= 1
            for i in reversed(range(self.product_list_shopee.rowCount())):
                self.product_list_shopee.removeRow(i) 
            UIFunctions.get_list_products_shopee(self)

    def add_to_product_push(self):
        x = self.product_list_shopee.selectedItems()
        l = []
        data = []
        for i in x:
            l.append(i.row())
        for p in l:
            o ={}
            o['image'] = self.img[p]
            o['name_product'] = self.name[p]
            o['id_product'] = self.ids[p]
            data.append(o)
        UIFunctions.check_shop_choose(self)
        Database_mongoDB.add_protuct_push(self,self.id_wp,shop_choose,data)
        UIFunctions.set_data_product_push(self)

    def del_from_product_push(self):
        UIFunctions.check_shop_choose(self)
        x = self.product_list_user.selectedItems()  
        l = []
        for i in x:
            l.append(i.row())
            self.product_list_user.removeRow(i.row())
        for k in l:
            Database_mongoDB.registered_Users_Collection.update({"_id": self.id_wp}, {"$unset": {f"shopee.{shop_choose}.list_push_product.{k}": 1}})
            Database_mongoDB.registered_Users_Collection.update({"_id": self.id_wp}, {"$pull": {f"shopee.{shop_choose}.list_push_product": None}})
        
        with open('temp//data.json') as f:
                data = json.load(f)
        x = Database_mongoDB.registered_Users_Collection.find({'_id': self.id_wp})
        for y in x:
            data['shopee'] = y['shopee']
        with open('temp//data.json', 'w') as f:
                    json.dump(data, f)
        

    def set_data_product_push(self):
        self.product_list_user.setRowCount(24)
        for k in range(self.product_list_user.rowCount()):
            self.product_list_user.setRowHeight(k, 90)
        if self.comboBox_user.currentText() != 'Chưa có tài khoản':
            with open('temp//data.json') as f:
                data = json.load(f)
            UIFunctions.check_shop_choose(self)
            if len(data['shopee'][shop_choose]['list_push_product']) !=0:
                s1 = data['shopee'][shop_choose]['list_push_product']
                img = []
                for row, x in enumerate(s1):
                    self.product_list_user.setItem(row, 1,QTableWidgetItem(x['name_product']))
                for x in s1:
                    img.append(x['image'])

                self.workerthread1 = WorkerThread(img,'product_list_user')
                self.workerthread1.start()
                self.workerthread1.img_complete.connect(self.update_img)  

    def set_data_user_shopee(self):
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
                self.btn_del_user.clicked.connect(lambda: UIFunctions.btn_del_user(self))
                self.tableWidget.setCellWidget(row,0,self.btn_del_user)
                self.btn_del_user.setStyleSheet('QPushButton { image: url(img//remove.png);background: transparent;}QPushButton:hover { image: url(img//remove_red.png);}')
                self.tableWidget.setItem(row, 1,QTableWidgetItem(data['id_sp']))
                self.tableWidget.setItem(row, 2,QTableWidgetItem(data['shop_name']))
                self.tableWidget.setItem(row, 3,QTableWidgetItem(data['shop_id']))
                self.tableWidget.setItem(row, 4,QTableWidgetItem(data['total_product']))
                self.tableWidget.setItem(row, 5,QTableWidgetItem(data['total_order']))
               
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
                    btn_gh.clicked.connect(lambda: UIFunctions.open_browser(self))
                    
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

    def set_comboBox_user(self):
        with open('temp//data.json') as f:
            data = json.load(f)

        self.comboBox_user.clear()    
        for x in range(len(data['shopee'])):
            if data['shopee'][x]['status_cookie'] == "True":
                self.comboBox_user.addItem(data['shopee'][x]['shop_name'])
                        
        if self.comboBox_user.count() == 0 :
            self.comboBox_user.addItem("Chưa có tài khoản") 

    def btn_del_user(self):
        x = QMessageBox.warning(self, 'MessageBox', "TẤT CẢ DỮ LIỆU SẼ MẤT \nBạn có chắc chắn muốn xóa tài khoản này không ?", QMessageBox.No , QMessageBox.Yes)
        if x == QMessageBox.Yes:
            button = self.sender()
            index = self.tableWidget.indexAt(button.pos())
            with open('temp//data.json') as f:
                data = json.load(f)

            Database_mongoDB.registered_Users_Collection.update({"_id": data['id_wp']}, {"$unset": {f"shopee.{index.row()}": 1}})
            Database_mongoDB.registered_Users_Collection.update({"_id": data['id_wp']}, {"$pull": {"shopee": None}})

            del data['shopee'][index.row()]
            with open('temp//data.json', 'w') as f:
                json.dump(data, f)

            for i in reversed(range(self.tableWidget.rowCount())):
                self.tableWidget.removeRow(i)  
                
            self.comboBox_user.addItem("Chưa có tài khoản") 
            UIFunctions.set_comboBox_user(self)
            UIFunctions.set_data_user_shopee(self)

    def set_data_rating_shopee(self):
        UIFunctions.check_shop_choose(self)
        with open('temp//data.json') as f:
            data = json.load(f)
            shopee = data['shopee']

        if len(shopee) != 0: 
  
            s1 = data['shopee'][shop_choose]['reply_rating']['rating_1star']
            s2 = data['shopee'][shop_choose]['reply_rating']['rating_2star']
            s3 = data['shopee'][shop_choose]['reply_rating']['rating_3star']
            s4 = data['shopee'][shop_choose]['reply_rating']['rating_4star']
            s5 = data['shopee'][shop_choose]['reply_rating']['rating_5star']

            self.tw_ratting1.setRowCount(len(s1) if len(s1) >3 else 3)  
            self.tw_ratting2.setRowCount(len(s2) if len(s2) >3 else 3)   
            self.tw_ratting3.setRowCount(len(s3) if len(s3) >3 else 3)
            self.tw_ratting4.setRowCount(len(s4) if len(s4) >3 else 3)
            self.tw_ratting5.setRowCount(len(s5) if len(s5) >3 else 3)

            for row, data in enumerate (s1):                               
                self.tw_ratting1.setItem(row, 1,QTableWidgetItem(str(row+1)))
                self.tw_ratting1.setItem(row, 2,QTableWidgetItem(data))
                self.btn_delete1 = QPushButton('')
                self.btn_delete1.clicked.connect(lambda: UIFunctions.delete1(self))
                self.tw_ratting1.setCellWidget(row,0,self.btn_delete1)
                self.btn_delete1.setStyleSheet('QPushButton { image: url(img//remove.png);background: transparent;}QPushButton:hover { image: url(img//remove_red.png);}')

            for row, data_2 in enumerate(s2):                                  
                self.tw_ratting2.setItem(row, 1,QTableWidgetItem(str(row+1)))
                self.tw_ratting2.setItem(row, 2,QTableWidgetItem(data_2))
                self.btn_delete2 = QPushButton('')
                self.btn_delete2.clicked.connect(lambda: UIFunctions.delete2(self))
                self.tw_ratting2.setCellWidget(row,0,self.btn_delete2)
                self.btn_delete2.setStyleSheet('QPushButton { image: url(img//remove.png);background: transparent;}QPushButton:hover { image: url(img//remove_red.png);}')          

            for row, data_3 in enumerate(s3):                             
                self.tw_ratting3.setItem(row, 1,QTableWidgetItem(str(row+1)))
                self.tw_ratting3.setItem(row, 2,QTableWidgetItem(data_3))
                self.btn_delete3 = QPushButton('')
                self.btn_delete3.clicked.connect(lambda: UIFunctions.delete3(self))
                self.tw_ratting3.setCellWidget(row,0,self.btn_delete3)
                self.btn_delete3.setStyleSheet('QPushButton { image: url(img//remove.png);background: transparent;}QPushButton:hover { image: url(img//remove_red.png);}')

            for row, data_4 in enumerate(s4):                              
                self.tw_ratting4.setItem(row, 1,QTableWidgetItem(str(row+1)))
                self.tw_ratting4.setItem(row, 2,QTableWidgetItem(data_4))
                self.btn_delete4 = QPushButton('')
                self.btn_delete4.clicked.connect(lambda: UIFunctions.delete4(self))
                self.tw_ratting4.setCellWidget(row,0,self.btn_delete4)
                self.btn_delete4.setStyleSheet('QPushButton { image: url(img//remove.png);background: transparent;}QPushButton:hover { image: url(img//remove_red.png);}')

            for row, data_5 in enumerate(s5):                               
                self.tw_ratting5.setItem(row, 1,QTableWidgetItem(str(row+1)))
                self.tw_ratting5.setItem(row, 2,QTableWidgetItem(data_5))
                self.btn_delete5 = QPushButton('')
                self.btn_delete5.clicked.connect(lambda: UIFunctions.delete5(self))
                self.tw_ratting5.setCellWidget(row,0,self.btn_delete5)
                self.btn_delete5.setStyleSheet('QPushButton { image: url(img//remove.png);background: transparent;}QPushButton:hover { image: url(img//remove_red.png);}')

        elif len(shopee) == 0:
            self.tw_ratting1.setRowCount(3)
            self.tw_ratting2.setRowCount(3)
            self.tw_ratting3.setRowCount(3)
            self.tw_ratting4.setRowCount(3)
            self.tw_ratting5.setRowCount(3)

                
    def pop_up_rating(self):
        from dashboard.dashboard import Popup_Rating
        self.ui = Popup_Rating()
        self.ui.show()
        self.ui.btn_send.clicked.connect(lambda: UIFunctions.set_data_rating_shopee(self))

    def delete1(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa nội dụng đánh giá này không", QMessageBox.No , QMessageBox.Yes)
        if x == QMessageBox.Yes:
            self.pos_table = self.tw_ratting1
            self.table_name = 'rating_1star'
            UIFunctions.delete_ratings(self)

    def delete2(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa nội dụng đánh giá này không", QMessageBox.No , QMessageBox.Yes)
        if x == QMessageBox.Yes:
            self.pos_table = self.tw_ratting2
            self.table_name = 'rating_2star'
            UIFunctions.delete_ratings(self)

    def delete3(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa nội dụng đánh giá này không", QMessageBox.No , QMessageBox.Yes)
        if x == QMessageBox.Yes:
            self.pos_table = self.tw_ratting3
            self.table_name = 'rating_3star'
            UIFunctions.delete_ratings(self)        

    def delete4(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa nội dụng đánh giá này không", QMessageBox.No , QMessageBox.Yes)
        if x == QMessageBox.Yes:
            self.pos_table = self.tw_ratting4
            self.table_name = 'rating_4star'
            UIFunctions.delete_ratings(self)

    def delete5(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa nội dụng đánh giá này không", QMessageBox.No , QMessageBox.Yes)
        if x == QMessageBox.Yes:
            self.pos_table = self.tw_ratting5
            self.table_name = 'rating_5star'
            UIFunctions.delete_ratings(self)

    def delete_ratings(self):     
        button = self.sender()
        index = self.pos_table.indexAt(button.pos())
        UIFunctions.check_shop_choose(self)
        with open('temp//data.json') as f:
            data = json.load(f)
            shopee = data['shopee']

        k = data['shopee'][shop_choose]['reply_rating'][self.table_name][index.row()]
        del data['shopee'][shop_choose]['reply_rating'][self.table_name][index.row()]
        with open('temp//data.json', 'w') as f:
            json.dump(data, f)
        Database_mongoDB.registered_Users_Collection.update_one(
            { '_id': data['id_wp'] },
            { '$pull': { f'shopee.{shop_choose}.reply_rating.{self.table_name}': k } }
            )
        for i in reversed(range(self.tableWidget.rowCount())):
            self.pos_table.removeRow(i) 
        
        UIFunctions.set_data_rating_shopee(self)    


    def change_theme(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        if data['theme'] == 'dark':
            data['theme'] = 'light'
        elif data['theme'] == 'light':
            data['theme'] = 'dark'
        with open('temp//data.json', 'w') as f:
            json.dump(data,f)
        from dashboard.dashboard import Dashboard
        self.dashboard = Dashboard()
        self.close()

    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        ## REMOVE ==> STANDARD TITLE BAR
        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            self.frame_label_top_btns.mouseDoubleClickEvent = dobleClickMaximizeRestore
        else:
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.frame_label_top_btns.setContentsMargins(8, 0, 0, 5)
            self.frame_label_top_btns.setMinimumHeight(42)
            self.frame_icon_top_bar.hide()
            self.frame_btns_right.hide()
            self.frame_size_grip.hide()


        ## SHOW ==> DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(30)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(1, 0, 0, 255))
        self.frame_main.setGraphicsEffect(self.shadow)

        ## ==> RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.frame_size_grip)
        self.sizegrip.setStyleSheet("width: 20px; height: 20px; margin 0px; padding: 0px;")

        ### ==> MINIMIZE
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())

        ## ==> MAXIMIZE/RESTORE
        self.btn_maximize_restore.clicked.connect(lambda: UIFunctions.maximize_restore(self))

        ## SHOW ==> CLOSE APPLICATION
        self.btn_close.clicked.connect(lambda: UIFunctions.close_App(self))

    def close_App(self):
        Database_mongoDB.close_db_connection(self)
        app = QApplication.instance()
        app.closeAllWindows()

class Style:

    style_bt_light = (
    """
    QPushButton {
        color: rgb(247, 247, 255); 
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 28px solid rgb(69, 65, 245);
        background-color: rgb(69, 65, 245);
        text-align: left;
        padding-left: 50px;
    }
    QPushButton[Active=true] {
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 28px solid rgb(69, 65, 245);
        border-right: 5px solid rgb(85, 170, 255);
        background-color: rgb(69, 65, 245);
        text-align: left;
        padding-left: 50px;
    }
    QPushButton:hover {
        background-color: rgb(69, 85, 245);
        border-left: 28px solid rgb(69, 85, 245);
    }
    QPushButton:pressed {
        background-color: rgb(85, 170, 255);
        border-left: 28px solid rgb(85, 170, 255);
    }
    """
    )

    style_bt_dark = (
    """
    QPushButton {
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 28px solid rgb(27, 29, 35);
        background-color: rgb(27, 29, 35);
        text-align: left;
        padding-left: 50px;
    }
    QPushButton[Active=true] {
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 28px solid rgb(27, 29, 35);
        border-right: 5px solid rgb(85, 170, 255);
        background-color: rgb(27, 29, 35);
        text-align: left;
        padding-left: 50px;
    }
    QPushButton:hover {
        background-color: rgb(33, 37, 43);
        border-left: 28px solid rgb(33, 37, 43);
    }
    QPushButton:pressed {
        background-color: rgb(85, 170, 255);
        border-left: 28px solid rgb(85, 170, 255);
    }
    """
    )

class WorkerThread(QThread):
    img_complete = pyqtSignal(list)

    def __init__(self,img,index):
        super().__init__()
        self.img = img
        self.index = index
    def run(self):
        for row , data_img in enumerate(self.img):
            url = f'https://cf.shopee.vn/file/{data_img}_tn'
            img = urllib.request.urlopen(url).read()
            l = [row,img,self.index]
            self.img_complete.emit(l)

class ThreadGetInfo(QThread):
    
    def __init__(self):
        super().__init__()

    def run(self):
        with open('temp//data.json') as f:
            d = json.load(f)
            k = d['shopee']
            if len(k) != 0:
                for i in range(len(k)):
                    cookie = k[i]['cookie']
                    r = backend.networks.Network.list_products_shopee(self,cookie,1)
                    if r['message'] == "success":
                        d['shopee'][i]['status_cookie'] = "True"
                        d['shopee'][i]['total_product'] = str(r['data']['page_info']['total'])
                        with open('temp//data.json', 'w') as f:
                            json.dump(d,f)
                        Database_mongoDB.find_and_updateDB(self,d['id_wp'],{f"shopee.{i}.status_cookie" : "True",f"shopee.{i}.total_product" : d['shopee'][i]['total_product']})
                    else:
                        d['shopee'][i]['status_cookie'] = "False"
                        with open('temp//data.json', 'w') as f:
                            json.dump(d,f)
                        Database_mongoDB.find_and_updateDB(self,d['id_wp'],{f"shopee.{i}.status_cookie" : "False"})

class ThreadGetListProduct(QThread):

    r_json = pyqtSignal(list)

    def __init__(self, cookie, page_number):
        super().__init__()
        self.c = cookie
        self.p = page_number

    def run(self):
        r = backend.networks.Network.list_products_shopee(self,self.c,self.p)
        l = [r,self.p]
        self.r_json.emit(l)

