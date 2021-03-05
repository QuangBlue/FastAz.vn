from dashboard.dashboard import *
from dashboard.style import *
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
        self.button.setStyleSheet(Style.style_bt.replace('ICON_REPLACE', icon))    
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
        with open('temp//data.json') as f:
            data = json.load(f)
        if len(data['shopee']) != 0:
            for x in range(len(data['shopee'])):
                if data['shopee'][x]['shop_name'] == self.comboBox_user.currentText():
                    shop_choose = x

    def set_data_product_push(self):
        self.tableWidget_product_push.setRowCount(24)
        for k in range(self.tableWidget_product_push.rowCount()):
            self.tableWidget_product_push.setRowHeight(k, 90)

        self.tableWidget_product_push.setColumnWidth(0, 50)
        self.tableWidget_product_push.setColumnWidth(1, 100)
        self.tableWidget_product_push.setColumnWidth(2, 800)
        self.tableWidget_product_push.setColumnWidth(3, 150)
        self.tableWidget_product_push.setColumnWidth(4, 150)
        self.tableWidget_product_push.setColumnWidth(5, 150)
        self.tableWidget_product_push.setColumnWidth(6, 150)
        with open('temp//data.json') as f:
            data = json.load(f)
        UIFunctions.check_shop_choose(self)
        if len(data['shopee']) != 0:         
            if len(data['shopee'][shop_choose]['list_push_product']) !=0:
                self.tableWidget_product_push.setRowCount(len(data['shopee'][shop_choose]['list_push_product']) if len(data['shopee'][shop_choose]['list_push_product']) > 24 else 24)
                for k in range(self.tableWidget_product_push.rowCount()):
                    self.tableWidget_product_push.setRowHeight(k, 90)              
                s1 = data['shopee'][shop_choose]['list_push_product']
                img = []
                for row, x in enumerate(s1):
                    self.btn_del_pp = QPushButton('')
                    self.btn_del_pp.clicked.connect(lambda: UIFunctions.btn_del_pp(self))
                    self.tableWidget_product_push.setCellWidget(row,0,self.btn_del_pp)
                    self.btn_del_pp.setStyleSheet('QPushButton { image: url(img//remove.png);background: transparent;}QPushButton:hover { image: url(img//remove_red.png);}')
                    self.tableWidget_product_push.setItem(row, 2,QTableWidgetItem(x['name']))
                    self.tableWidget_product_push.setItem(row, 3,QTableWidgetItem(x['parent_sku']))
                    self.tableWidget_product_push.setItem(row, 4,QTableWidgetItem(str(x['stock'])))
                    self.tableWidget_product_push.setItem(row, 5,QTableWidgetItem(x['normal_price']))
                    self.tableWidget_product_push.setItem(row, 6,QTableWidgetItem(x['promotion_price']))
                    self.tableWidget_product_push.setItem(row, 7,QTableWidgetItem(str(x['sold'])))
                for x in s1:
                    img.append(x['image'])
                self.workerthread1 = WorkerThread(img,'product_list_user')
                self.workerthread1.start()
                self.workerthread1.img_complete.connect(self.update_img)  
        UIFunctions.writeLog(self,'Tải sản phẩm đẩy')
    def btn_del_pp(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa sản phẩm này không ?", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)        
        with open('temp//data.json') as f:
            data = json.load(f)
        
        if x == QMessageBox.Yes:
            button = self.sender()
            index = self.tableWidget_product_push.indexAt(button.pos())
            UIFunctions.check_shop_choose(self)

            self.tableWidget_product_push.removeRow(index.row())

            Database_mongoDB.registered_Users_Collection.update({"_id": data['id_wp']}, {"$unset": {f"shopee.{shop_choose}.list_push_product.{index.row()}": 1}})
            Database_mongoDB.registered_Users_Collection.update({"_id": data['id_wp']}, {"$pull": {f"shopee.{shop_choose}.list_push_product": None}})
            UIFunctions.writeLog(self,'Xóa sản phẩm đẩy')

        x = Database_mongoDB.registered_Users_Collection.find({'_id': data['id_wp']})
        for y in x:
            data['shopee'] = y['shopee']
        with open('temp//data.json', 'w') as f:
                    json.dump(data, f)

    def popup_add_product_push(self):
        UIFunctions.check_shop_choose(self)

        from dashboard.dashboard import Popup_Product
        self.ui = Popup_Product(shop_choose)
        self.ui.show()
        self.ui.btn_confirm.clicked.connect(lambda: UIFunctions.set_data_product_push(self))

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

        UIFunctions.writeLog(self,'Tải dữ liệu đánh giá Shopee')

                
    def pop_up_rating(self):
        from dashboard.dashboard import Popup_Rating
        self.ui = Popup_Rating()
        self.ui.show()
        self.ui.btn_send.clicked.connect(lambda: UIFunctions.set_data_rating_shopee(self))

    def delete1(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa nội dụng đánh giá này không", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if x == QMessageBox.Yes:
            self.pos_table = self.tw_ratting1
            self.table_name = 'rating_1star'
            UIFunctions.delete_ratings(self)

    def delete2(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa nội dụng đánh giá này không", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if x == QMessageBox.Yes:
            self.pos_table = self.tw_ratting2
            self.table_name = 'rating_2star'
            UIFunctions.delete_ratings(self)

    def delete3(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa nội dụng đánh giá này không", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if x == QMessageBox.Yes:
            self.pos_table = self.tw_ratting3
            self.table_name = 'rating_3star'
            UIFunctions.delete_ratings(self)        

    def delete4(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa nội dụng đánh giá này không", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        if x == QMessageBox.Yes:
            self.pos_table = self.tw_ratting4
            self.table_name = 'rating_4star'
            UIFunctions.delete_ratings(self)

    def delete5(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa nội dụng đánh giá này không", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
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
        UIFunctions.writeLog(self,'Xóa đánh giá Shopee')
        UIFunctions.set_data_rating_shopee(self)    


    def change_theme(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        if data['theme'] == 'dark':
            data['theme'] = 'light'
            self.frame_main.setStyleSheet(Style.main_light)
            self.btn_theme.setText('Dark Theme')
        elif data['theme'] == 'light':
            data['theme'] = 'dark'
            self.frame_main.setStyleSheet(Style.main_dark)
            self.btn_theme.setText('Light Theme')
        with open('temp//data.json', 'w') as f:
            json.dump(data,f)
        UIFunctions.writeLog(self,'Đổi giao diện')
    def check_theme(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        if data['theme'] == 'dark':
            self.frame_main.setStyleSheet(Style.main_dark)
            self.btn_theme.setText('Light Theme')
        elif data['theme'] == 'light':
            self.frame_main.setStyleSheet(Style.main_light)
            self.btn_theme.setText('Dark Theme')

    def writeLog(self,textLog,w=0):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        log = f'{current_time} - {textLog}'
        if w == 0:
            self.textLogSystem.appendPlainText(log)
        elif w == 1:
            self.textLogFunction.appendPlainText(log)

    def openBrowser(self):
        if len(self.page_browser.findChildren(QWebEngineView)) > 0 :
            for i in self.page_browser.findChildren(QWebEngineView):
                i.close()
        with open('temp//data.json') as f:
            data = json.load(f)
        UIFunctions.check_shop_choose(self)   
        if len(data['shopee']) != 0:
            def btnBrowserHome(): 
                self.webEngineView.setUrl(QUrl("https://banhang.shopee.vn")) 
            def updateUrlBar(q): 
                self.urlBar.setText(q.toString()) 
            self.webEngineView = MyWebView(data['shopee'][shop_choose]['pathName'])
            print(data['shopee'][shop_choose]['pathName'])
            self.layoutBrowers.addWidget(self.webEngineView)
            self.urlBar.setText("https://banhang.shopee.vn")
            self.webEngineView.urlChanged.connect(updateUrlBar) 
            self.browserBack.clicked.connect(self.webEngineView.back) 
            self.browserForward.clicked.connect(self.webEngineView.forward)
            self.browserReload.clicked.connect(self.webEngineView.reload) 
            self.browserHome.clicked.connect(btnBrowserHome)
            # self.openBrowser.clicked.connect()
            self.webEngineView.show()
            UIFunctions.writeLog(self,f"Mở browser với profile {data['shopee'][shop_choose]['pathName']}")

    def countTextChatBot(self,obj,layout):
        r = obj.findChildren(QPlainTextEdit)
        UIFunctions.addFrameText(self,len(r)+1,obj,layout)

    def addFrameText(self,count,obj,layout,text=''):
        font = QFont()
        font.setFamily(u"Nunito")
        font.setPointSize(16)
        frameT = QHBoxLayout()
        plainText = QPlainTextEdit()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        plainText.setSizePolicy(sizePolicy)
        plainText.setMinimumSize(QSize(0,200))
        plainText.setLayoutDirection(Qt.LeftToRight)
        plainText.setObjectName(f"plainText_{count}")
        plainText.setFont(font)
        plainText.setPlaceholderText('Nội dung sẽ gửi cho khách hàng khi đơn hàng có trạng thái mới.')
        plainText.setFocus()
        plainText.setPlainText(text)
        label = QLabel(f"{count}#")
        label.setObjectName(f"label_{count}")
        label.setFont(font)
        btn = QPushButton('')
        btn.setObjectName(f"_{count}")
        btn.setStyleSheet('QPushButton { background: transparent;}')
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        btn.setSizePolicy(sizePolicy1)
        btn.setIcon(QIcon('img/clear.png')) 
        btn.clicked.connect(lambda : UIFunctions.delPlainTextEdit(self,obj,layout))       
        frameT.addWidget(label)
        frameT.addWidget(btn)
        layout.addLayout(frameT)
        layout.addWidget(plainText)

    def delPlainTextEdit(self,obj,layout):
        btnWidget = self.sender()
        objName = btnWidget.objectName()
        layout.removeWidget(obj.findChildren(QLabel , f'label{objName}')[0]) 
        layout.removeWidget(obj.findChildren(QPushButton, f'{objName}')[0])
        layout.removeWidget(obj.findChildren(QPlainTextEdit, f'plainText{objName}')[0])
        UIFunctions.writeLog(self,'Xóa nội dụng chat bot')

    def updateToDataJson(self,_id):
        with open('temp//data.json') as f:
            data = json.load(f)
        x = Database_mongoDB.registered_Users_Collection.find({'_id': _id})
        for y in x:
            data['shopee'] = y['shopee']
        with open('temp//data.json', 'w') as f:
            json.dump(data, f)


    def show_popup(self,title,info,notification,c=True):   
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

    def setChatBotPlainText(self):
        try:
            with open('temp//data.json') as f:
                data = json.load(f)
            UIFunctions.check_shop_choose(self)
            obj = [
            self.frameOrderNew_obj,
            self.frameOrderReady_obj,
            self.frameOrderShipping_obj,
            self.frameOrderSuccess_obj,
            self.frameOrderCancel_obj,
            ]
            layout = [
            self.frameOrderNew,
            self.frameOrderReady,
            self.frameOrderShipping,
            self.frameOrderSuccess,
            self.frameOrderCancel,
            ]         
            new = data['shopee'][shop_choose]['orderChatBotList']['textOrderNew']
            ready = data['shopee'][shop_choose]['orderChatBotList']['textOrderReady']
            shipping = data['shopee'][shop_choose]['orderChatBotList']['textOrderShipping']
            success = data['shopee'][shop_choose]['orderChatBotList']['textOrderSuccess']
            cancel = data['shopee'][shop_choose]['orderChatBotList']['textOrderCancel']
            dataText = [new,ready,shipping,success,cancel]
            for o , l , d in zip(obj,layout,dataText):
                count = 1
                for i in d:
                    UIFunctions.addFrameText(self,count,o,l,i)
                    count += 1
            UIFunctions.writeLog(self,f"Tải nội dung ChatBot cho account {data['shopee'][shop_choose]['shop_name']}")   
        except: 
            pass
           
    def btnSaveChatBot(self):
        UIFunctions.check_shop_choose(self)
        with open('temp//data.json') as f:
            data = json.load(f)

        textOrderNew = []
        textOrderReady = []
        textOrderShipping = []
        textOrderSuccess = []
        textOrderCancel = []

        obj = [
            self.frameOrderNew_obj,
            self.frameOrderReady_obj,
            self.frameOrderShipping_obj,
            self.frameOrderSuccess_obj,
            self.frameOrderCancel_obj,
        ]

        for frame in obj:
            for textData in frame.findChildren(QPlainTextEdit):
                if len(textData.toPlainText()) != 0:
                    if frame == self.frameOrderNew_obj:
                        textOrderNew.append(textData.toPlainText())
                    elif frame == self.frameOrderReady_obj:
                        textOrderReady.append(textData.toPlainText())
                    elif frame == self.frameOrderShipping_obj:
                        textOrderShipping.append(textData.toPlainText())
                    elif frame == self.frameOrderSuccess_obj:
                        textOrderSuccess.append(textData.toPlainText())
                    elif frame == self.frameOrderCancel_obj:
                        textOrderCancel.append(textData.toPlainText())

        r = Database_mongoDB.registered_Users_Collection.update(
            { '_id': data['id_wp'] },
            { '$set': { 
                f'shopee.{shop_choose}.orderChatBotList.textOrderNew': textOrderNew, 
                f'shopee.{shop_choose}.orderChatBotList.textOrderReady': textOrderReady,
                f'shopee.{shop_choose}.orderChatBotList.textOrderShipping': textOrderShipping,
                f'shopee.{shop_choose}.orderChatBotList.textOrderSuccess': textOrderSuccess,
                f'shopee.{shop_choose}.orderChatBotList.textOrderCancel': textOrderCancel, 
                }},
            upsert=True  
            )     
        
        if r['updatedExisting'] == True:
            UIFunctions.updateToDataJson(self,data['id_wp'])
            UIFunctions.show_popup(self,"Thành Công","Lưu nội dung Thành Công","Tất cả nội dung trả lời đã được lưu Thành Công",True)
            UIFunctions.writeLog(self,'Lưu thành công nội dụng ChatBot')
        else:
            UIFunctions.show_popup(self,"Không Thành Công","Không lưu được nội dung","Vui lòng liên hệ fanpage để được trợ giúp",False)
            UIFunctions.writeLog(self,'Không lưu thành công nội dụng ChatBot')
    def setStyleButtonChatBot(self,objectName):
        for w in self.frameButtonChatBot.findChildren(QPushButton):
            if w.objectName() != objectName:
                w.setStyleSheet('')
            if w.objectName() == objectName:
                w.setStyleSheet('background-color: rgb(217, 38, 0);')

    def btnChatBot(self):
        btn = self.sender()

        if btn.objectName() == 'btnOrderNew':
            self.stackedWidgetChatBot.setCurrentIndex(0)
            UIFunctions.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderReady':
            self.stackedWidgetChatBot.setCurrentIndex(4)
            UIFunctions.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderShipping':
            self.stackedWidgetChatBot.setCurrentIndex(3)
            UIFunctions.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderSuccess':
            self.stackedWidgetChatBot.setCurrentIndex(2)
            UIFunctions.setStyleButtonChatBot(self,btn.objectName())

        elif btn.objectName() == 'btnOrderCancel':
            self.stackedWidgetChatBot.setCurrentIndex(1)
            UIFunctions.setStyleButtonChatBot(self,btn.objectName())

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
        # self.shadow = QGraphicsDropShadowEffect(self)
        # self.shadow.setBlurRadius(30)
        # self.shadow.setXOffset(0)
        # self.shadow.setYOffset(0)
        # self.shadow.setColor(QColor(1, 0, 0, 255))
        # self.frame_main.setGraphicsEffect(self.shadow)

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


class MyWebView(QWebEngineView):
    def __init__(self,pathName):
        super(MyWebView, self).__init__()
        profile = QWebEngineProfile(pathName, self)
        webpage = QWebEnginePage(profile, self)
        self.setPage(webpage)
        self.setUrl(QUrl("https://banhang.shopee.vn")) 
        self.setAttribute(Qt.WA_DeleteOnClose)