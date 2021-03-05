from main_pyqt5 import *
from dashboard.s_db import *
from dashboard.style import *
from dashboard.accountShopee import *
from dashboard.browser import Browser
from data_example import *
from backend.MongoDB_Setup import * 

status_user = 1
status_rating = 1
numbers = 1

class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard,self).__init__()
        loadUi("ui//dashboard_screen_main.ui",self)
        UIFunctions.check_theme(self)
        self.resize(1920, 1080)
        QFontDatabase.addApplicationFont('font/Nunito/Nunito-Regular.ttf')
        QFontDatabase.addApplicationFont('font/Nunito/Nunito-Regular.ttf')
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
        UIFunctions.addNewMenu(self, "Trình duyệt", "btn_browser", "url(:/icon/cil-browser.png)", True)
        # UIFunctions.addNewMenu(self, "Log", "btn_log", "url(:/icon/cil-settings.png)", False)
        UIFunctions.addNewMenu(self, "Setting", "btn_settings", "url(:/icon/cil-settings.png)", False)


        # ########################################################################
        ## SHOPEE SHOW-OFF
        # ########################################################################
        # logTextBox = QTextEditLogger(self)
        # logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        # logging.getLogger().addHandler(logTextBox)
        # logging.getLogger().setLevel(logging.DEBUG)

        # self.button_log = QPushButton()
        # self.frame_log.addWidget(logTextBox.widget)

        # self.table_widget_test = TableWidgetDragRows()
        # self.table_test.addWidget(self.table_widget_test)

        # QTimer.singleShot(100, lambda: UIFunctions.table_widget_test(self))

        self.addTextOrderNew.clicked.connect(lambda : UIFunctions.countTextChatBot(self,self.frameOrderNew_obj,self.frameOrderNew))
        self.addTextOrderCancel.clicked.connect(lambda : UIFunctions.countTextChatBot(self,self.frameOrderCancel_obj,self.frameOrderCancel))
        self.addTextOrderReady.clicked.connect(lambda : UIFunctions.countTextChatBot(self,self.frameOrderReady_obj,self.frameOrderReady))
        self.addTextOrderSuccess.clicked.connect(lambda : UIFunctions.countTextChatBot(self,self.frameOrderSuccess_obj,self.frameOrderSuccess))
        self.addTextOrderShipping.clicked.connect(lambda : UIFunctions.countTextChatBot(self,self.frameOrderShipping_obj,self.frameOrderShipping))


        # ########################################################################
        ## SET SHADOW FOR FRAME CHAT BOT
        # ########################################################################


        # listShadow = [
        #     self.frameButtonChatBot,
        #     self.frameTitleOrderNew,self.scrollAreaOrderNew,
        #     self.frameTitleOrderCancel,self.scrollAreaOrderCancel,
        #     self.frameTitleOrderReady,self.scrollAreaOrderReady,
        #     self.frameTitleOrderSuccess,self.scrollAreaOrderSuccess,
        #     self.frameTitleOrderShipping,self.scrollAreaOrderShipping,
        #     ]

        # for child in listShadow:
        #     shadow = QGraphicsDropShadowEffect()
        #     shadow.setBlurRadius(12)
        #     shadow.setXOffset(0)
        #     shadow.setYOffset(0)
        #     shadow.setColor(QColor(0, 0, 0, 30))
        #     child.setGraphicsEffect(shadow)

        # ########################################################################
        ## FIRST LAUNCH APP - START FUNCTION FOR UPDATE DATA MAIN WINDOW
        # ########################################################################
        

        QTimer.singleShot(100, lambda: UserShopee.setDataUserShopee(self))
        UserShopee.setComboBoxUser(self)

        QTimer.singleShot(100, lambda: UIFunctions.set_data_rating_shopee(self))
        QTimer.singleShot(100, lambda: UIFunctions.set_data_product_push(self))
        QTimer.singleShot(100, lambda: UIFunctions.setChatBotPlainText(self))
        QTimer.singleShot(100, lambda: UIFunctions.openBrowser(self))


        # ########################################################################
        ## SETUP SIGNAL BUTTON
        # ########################################################################

        self.btn_add_product_push.clicked.connect(lambda: UIFunctions.popup_add_product_push(self))
        self.btn_add_rating.clicked.connect(lambda: UIFunctions.pop_up_rating(self))
        self.btn_apply_all_rating.clicked.connect(lambda: UIFunctions.set_data_rating_shopee(self))
        
        Dashboard.comboBox_user_text = self.comboBox_user.currentText()

        # ########################################################################
        ## BUTTON SIGNAL CHAT BOT
        # ########################################################################

        self.btnOrderNew.clicked.connect(lambda: UIFunctions.btnChatBot(self))
        self.btnOrderReady.clicked.connect(lambda: UIFunctions.btnChatBot(self))
        self.btnOrderShipping.clicked.connect(lambda: UIFunctions.btnChatBot(self))
        self.btnOrderSuccess.clicked.connect(lambda: UIFunctions.btnChatBot(self))
        self.btnOrderCancel.clicked.connect(lambda: UIFunctions.btnChatBot(self))

        self.stackedWidgetChatBot.setCurrentIndex(0)

        self.btnSaveOrderNew.clicked.connect(lambda: UIFunctions.btnSaveChatBot(self))
        self.btnSaveOrderReady.clicked.connect(lambda: UIFunctions.btnSaveChatBot(self))
        self.btnSaveOrderShipping.clicked.connect(lambda: UIFunctions.btnSaveChatBot(self))
        self.btnSaveOrderSuccess.clicked.connect(lambda: UIFunctions.btnSaveChatBot(self))
        self.btnSaveOrderCancel.clicked.connect(lambda: UIFunctions.btnSaveChatBot(self))


        # ########################################################################
        ## BUTTON CHANGE THEME
        # ########################################################################

        self.btn_theme.clicked.connect(lambda: UIFunctions.change_theme(self))

        # ########################################################################
        ## SETUP NEW THREAD FOR UPDATE ACCOUNT SHOPEE INFO
        # ########################################################################

        self.threadgetinfo = ThreadGetInfo()
        self.threadgetinfo.start()
        self.threadgetinfo.finished.connect(lambda: UserShopee.setDataUserShopee(self))


        # ########################################################################
        ## SET UPDATE WHEN COMBOX CHANGE
        # ########################################################################
        self.comboBox_user.textActivated.connect(lambda: self.change_comboBox() )


        #############################################################
        ## ICON OR AVARTA OF USER
        # ########################################################################

        UIFunctions.userIcon(self)

        # ########################################################################
        ## HIDE TITLEBAR
        # ########################################################################
        UIFunctions.removeTitleBar(self,True)

        # ########################################################################
        ## THIỆT LẬP TÊN CỬA SỔ VÀ THÔNG TIN THÔNG BÁO
        # ########################################################################
        self.setWindowTitle('FastAz.vn - Ứng dụng bán hàng chuyên nghiệp')
        UIFunctions.labelTitle(self, 'FastAz.vn - Ứng dụng bán hàng chuyên nghiệp')
        UIFunctions.labelDescription(self, 'Mọi câu hỏi hoặc khó khăn vui lòng liên hệ Fanpage FastAz.Vn - Ứng dụng hỗ trợ bán hàng chuyên nghiệp')

        # ########################################################################
        ## MOVE WINDOW
        # ########################################################################
        def moveWindow(event):
            if self.isMaximized() == False:
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()
        self.frame_label_top_btns.mouseMoveEvent = moveWindow

        # ########################################################################
        ## BUTTON TOGGLE
        # ########################################################################
        self.btn_toggle_menu.clicked.connect(lambda: UIFunctions.toggleMenu(self, 220, True))

        
        # ########################################################################
        ## BUTTON OPEN BROWER --> ADD USER SHOPEE
        # ########################################################################

        self.btn_add_user.clicked.connect(lambda: UserShopee.openBrowserAddUserShopee(self))

        # ########################################################################
        ## SELECT DEFAULT MENU
        # ########################################################################
        
        UIFunctions.selectStandardMenu(self, "btn_new_user_shopee")
        self.stackedWidget.setCurrentWidget(self.page_new_user_shopee)

        # ########################################################################
        ## FUNCTION OF MAIN WINDOW
        # ########################################################################
        UIFunctions.uiDefinitions(self)
        self.show()

    def test(self):
        logging.debug('damn, a bug')
        logging.info('something to remember')
        logging.warning('that\'s not right')
        logging.error('foobar')


    def update_list_products_shopee(self, l):
        self.r = l[0]
        self.page_number = l[1]

        a = self.r['data']['page_info']['total']

        page_size = 1 if a <= 24 else (a // 24) +1
        self.btn_back.setEnabled(False) if self.page_number == 1 else self.btn_back.setEnabled(True)
        self.btn_forward.setEnabled(False) if self.page_number == page_size else self.btn_forward.setEnabled(True)

        if len(self.r['data']['list']) != 0:
            self.name = []
            self.img = []  
            self.ids = []  
            for x in range(len(self.r['data']['list'])):
                self.name.append(self.r['data']['list'][x]['name'])
                self.img.append(self.r['data']['list'][x]['images'][0])
                self.ids.append(self.r['data']['list'][x]['id'])
            for row ,data_name in enumerate(self.name):                
                self.product_list_shopee.setItem(row, 1,QTableWidgetItem(data_name))

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

        if l[2] == "product_list_shopee":
            self.product_list_shopee.setCellWidget(l[0],0,imgLabel)
        elif l[2] == 'product_list_user':
            self.tableWidget_product_push.setCellWidget(l[0],1,imgLabel)

 
    def change_comboBox(self):
        print('xxxxxx')
        Dashboard.comboBox_user_text = self.comboBox_user.currentText()
        l = [ self.tw_ratting1, self.tw_ratting1,self.tw_ratting3,self.tw_ratting4,self.tw_ratting5,self.tableWidget_product_push]
        for x in l:
            for i in reversed(range(x.rowCount())):
                x.removeRow(i)

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
        for o , l in zip(obj, layout):
            for i in range(len(o.findChildren(QPlainTextEdit))):
                l.removeWidget(o.findChildren(QPlainTextEdit)[0])
                l.removeWidget(o.findChildren(QLabel)[0])
                l.removeWidget(o.findChildren(QPushButton)[0])

            # self.layoutBrowser.removeWidget(self.page_browser.findChildren(QWebEngineView, 'browserShopee')[0])



        QTimer.singleShot(100, lambda: UIFunctions.set_data_rating_shopee(self))
        QTimer.singleShot(100, lambda: UIFunctions.set_data_product_push(self))
        QTimer.singleShot(100, lambda: UIFunctions.setChatBotPlainText(self))
        QTimer.singleShot(100, lambda: UIFunctions.openBrowser(self))
 
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
            if self.comboBox_user.count() == 0 :
                r = QMessageBox.warning(self, 'MessageBox', "BẠN CHƯA THÊM TÀI KHOẢN.\nVui lòng thêm ít nhất 1 tài khoản để sử dụng", QMessageBox.Ok, QMessageBox.Ok)
            else:        
                self.stackedWidget.setCurrentWidget(self.page_reply_ratting)
                UIFunctions.resetStyle(self, "btn_reply_ratting")
                UIFunctions.labelPage(self, "Trả lời Đánh giá")
                btnWidget.setStyleSheet(UIFunctions.selectMenu(self, btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_push_product":
            if self.comboBox_user.count() == 0 :
                r = QMessageBox.warning(self, 'MessageBox', "BẠN CHƯA THÊM TÀI KHOẢN.\nVui lòng thêm ít nhất 1 tài khoản để sử dụng", QMessageBox.Ok, QMessageBox.Ok)
            else: 
                
                self.stackedWidget.setCurrentWidget(self.page_push_product)
                UIFunctions.resetStyle(self, "btn_push_product")
                UIFunctions.labelPage(self, "Đẩy sản phẩm")
                btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))           
                
        if btnWidget.objectName() == "btn_chat_bot":
            if self.comboBox_user.count() == 0 :
                r = QMessageBox.warning(self, 'MessageBox', "BẠN CHƯA THÊM TÀI KHOẢN.\nVui lòng thêm ít nhất 1 tài khoản để sử dụng", QMessageBox.Ok, QMessageBox.Ok)
            else:
                self.stackedWidget.setCurrentWidget(self.page_chat_bot)
                UIFunctions.resetStyle(self, "btn_chat_bot")
                UIFunctions.labelPage(self, "Chat bot")
                btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_browser":
            if self.comboBox_user.count() == 0 :
                r = QMessageBox.warning(self, 'MessageBox', "BẠN CHƯA THÊM TÀI KHOẢN.\nVui lòng thêm ít nhất 1 tài khoản để sử dụng", QMessageBox.Ok, QMessageBox.Ok)
            else:
                self.stackedWidget.setCurrentWidget(self.page_browser)
                UIFunctions.resetStyle(self, "btn_browser")
                UIFunctions.labelPage(self, "Browser")
                btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))
                # UIFunctions.openBrowser(self)


        # if btnWidget.objectName() == "btn_log":
        #     self.stackedWidget.setCurrentWidget(self.page_log)
        #     UIFunctions.resetStyle(self, "btn_log")
        #     UIFunctions.labelPage(self, "Log")
        #     btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_settings":
            self.stackedWidget.setCurrentWidget(self.page_log)
            UIFunctions.resetStyle(self, "btn_settings")
            UIFunctions.labelPage(self, "Setting")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))            


class Popup_Rating(QMainWindow):
    def __init__(self):
        super(Popup_Rating,self).__init__()
        loadUi("ui//popup_ratting.ui",self)
        self.btn_send.clicked.connect(self.send_info_ratting)
        self.check_theme()

    def send_info_ratting(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        id_db = data['id_wp']
        new_rating = self.plainTextEdit_ratting.toPlainText().replace("\n",". ")
        if self.comboBox_ratting.currentText() == "Đánh giá 1 sao":
            select = 'rating_1star'
        elif self.comboBox_ratting.currentText() == "Đánh giá 2 sao":
            select = 'rating_2star' 
        elif self.comboBox_ratting.currentText() == "Đánh giá 3 sao":
            select = 'rating_3star'
        elif self.comboBox_ratting.currentText() == "Đánh giá 4 sao":
            select = 'rating_4star'  
        elif self.comboBox_ratting.currentText() == "Đánh giá 5 sao":
            select = 'rating_5star'

        if len(new_rating) > 10 and len(new_rating) < 500 :
            for x in range(len(data['shopee'])):
                if data['shopee'][x]['shop_name'] == Dashboard.comboBox_user_text:
                    k = Database_mongoDB.registered_Users_Collection.find_one({'_id':id_db})
                    k['shopee'][x]['reply_rating'][select].append(new_rating)
                    data['shopee'][x]['reply_rating'][select].append(new_rating)
                    with open('temp//data.json', 'w') as f:
                        json.dump(data, f)
                    Database_mongoDB.registered_Users_Collection.replace_one({'_id':id_db},k,upsert = True)
                    self.show_popup('Thành công','Thành công',f'Đã thêm thành công nội dụng trả lời cho {self.comboBox_ratting.currentText()}',True)
                    self.close()
        else:
            self.show_popup('Lỗi','Lỗi', 'Câu trả lời phải hơn 10 ký tự và nhỏ hơn 500 ký tự',False)


    def show_popup(self,title,info,notification,c=True):
        self.msg = QMessageBox()
        self.msg.setWindowTitle(title)
        self.msg.setText(notification)
        self.msg.setInformativeText(info)
        if c == True:
            self.msg.setIconPixmap(QPixmap("img//success.png"))
        else:
            self.msg.setIconPixmap(QPixmap("img//warning.png"))
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()

    def check_theme(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        if data['theme'] == 'dark':
            self.centralwidget.setStyleSheet(Style.rating_dark)
        elif data['theme'] == 'light':
            self.centralwidget.setStyleSheet(Style.rating_light)
         

# class QTextEditLogger(logging.Handler):
#     def __init__(self, parent):
#         super().__init__()
#         self.widget = QPlainTextEdit(parent)
#         self.widget.setReadOnly(True)

#     def emit(self, record):
#         msg = self.format(record)
#         self.widget.appendPlainText(msg)

class Popup_Product(QMainWindow):
    def __init__(self,shop_choose):
        super(Popup_Product,self,).__init__()
        loadUi("ui//popup_product_push.ui",self)
        self.resize(1700, 1000)
        self.cc = shop_choose
        self.get_list_products_shopee()

        self.btn_forward.clicked.connect(lambda : self.next_page())
        self.btn_back.clicked.connect(lambda : self.back_page())

        self.btn_confirm.clicked.connect(lambda : self.add_to_product_push())
        self.btn_cancel.clicked.connect(lambda : self.close())

    def get_list_products_shopee(self):
        self.tableWidget_product_push_shopee.setRowCount(24)
        for k in range(self.tableWidget_product_push_shopee.rowCount()):
            self.tableWidget_product_push_shopee.setRowHeight(k, 90)

        self.tableWidget_product_push_shopee.setColumnWidth(0, 50)
        self.tableWidget_product_push_shopee.setColumnWidth(1, 100)
        self.tableWidget_product_push_shopee.setColumnWidth(2, 700)
        self.tableWidget_product_push_shopee.setColumnWidth(3, 150)
        self.tableWidget_product_push_shopee.setColumnWidth(4, 150)
        self.tableWidget_product_push_shopee.setColumnWidth(5, 150)
        self.tableWidget_product_push_shopee.setColumnWidth(6, 150)

        self.tableWidget_product_push_shopee.setItem(0, 2,QTableWidgetItem("Đang tải dữ liệu ...."))
        
        global numbers
        
        with open('temp//data.json') as f:
            data = json.load(f)
            self.id_wp = data['id_wp']
            
            if len(data['shopee']) != 0:
                c = data['shopee'][self.cc]['cookie']
                
                self.worker_product = ThreadGetListProduct(c,numbers)
                self.worker_product.start()
                self.worker_product.r_json.connect(self.update_list_products_shopee)
    

    def update_list_products_shopee(self, l):
        self.r = l[0]
        self.page_number = l[1]

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
            data.append(k)
        r , change = Database_mongoDB.add_protuct_push(self,self.id_wp,self.cc,data)

        if r['updatedExisting'] == True:
            self.tableWidget_product_push_shopee.clearSelection()
            duplicate = len(set(l)) - change
            if duplicate == 0 :
                self.show_popup("Thành Công","Thêm sản phẩm thành công",f"{change} sản phẩm được chọn đã thêm thành công",True)
            else:
                self.show_popup("Thành Công","Thêm sản phẩm thành công",f"{change} sản phẩm thêm thành công và {duplicate} sản phẩm bị trùng ",True)    
        else:
            self.show_popup("Không Thành Công","Thêm sản phẩm không thành công","Vui lòng liên hệ fanpage để được trợ giúp",False)

    
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

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()