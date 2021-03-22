from main_pyqt5 import *
from dashboard.s_db import UIFunctions
from dashboard.style import Style
from dashboard.accountShopee import UserShopee
from dashboard.replyRating import ReplyRating
from dashboard.chatBot import ChatBot
from dashboard.productPush import ProductPush
from dashboard.browser import Browser
from data_example import *
from backend.MongoDB_Setup import * 

status_user = 1
status_rating = 1
shop_choose = 0

class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard,self).__init__()
        loadUi("ui//dashboard_screen_main.ui",self)
        UIFunctions.check_theme(self)
        self.resize(1280, 720)
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
        UIFunctions.addNewMenu(self, "Trả lời Đánh giá", "btn_reply_rating", "url(:/icon/cil-star.png)", True)
        UIFunctions.addNewMenu(self, "Đẩy sản phẩm", "btn_push_product", "url(:/icon/cil-chevron-double-up-alt.png)", True)
        UIFunctions.addNewMenu(self, "Chat bot", "btn_chat_bot", "url(:/icon/cil-mood-very-good.png)", True)
        UIFunctions.addNewMenu(self, "Trình duyệt", "btn_browser", "url(:/icon/cil-browser.png)", True)
        UIFunctions.addNewMenu(self, "Log", "btn_log", "url(:/icon/cil-settings.png)", False)
        UIFunctions.addNewMenu(self, "Setting", "btn_settings", "url(:/icon/cil-settings.png)", False)



        self.workerPushProduct = {}
        self.workerRealyReviews = {}


        # ########################################################################
        ## SHOPEE SHOW-OFF
        # ########################################################################

        self.btnPushProductSwitch = Toggle()
        self.btnPushProductSwitch.setObjectName('pushProductSwitch')
        self.activePushProductLayout.addWidget(self.btnPushProductSwitch)
        self.btnPushProductSwitch.setFocusPolicy(Qt.NoFocus)
        self.btnPushProductSwitch.clicked.connect(lambda: UIFunctions.setSwitchEnable(self))

        self.btnReplyRatingSwitch = Toggle()
        self.btnReplyRatingSwitch.setObjectName('replyRatingSwitch')
        self.activeReplyRatingLayout.addWidget(self.btnReplyRatingSwitch)
        self.btnReplyRatingSwitch.setFocusPolicy(Qt.NoFocus)
        self.btnReplyRatingSwitch.clicked.connect(lambda: UIFunctions.setSwitchEnable(self))

        self.btnChatBotSwitch = Toggle()
        self.btnChatBotSwitch.setObjectName('chatBotSwitch')
        self.activeChatBotLayout.addWidget(self.btnChatBotSwitch)
        self.btnChatBotSwitch.setFocusPolicy(Qt.NoFocus)
        self.btnChatBotSwitch.clicked.connect(lambda: UIFunctions.setSwitchEnable(self))

        self.addTextOrderNew.clicked.connect(lambda : UIFunctions.countFrameText(self,self.frameOrderNew_obj,self.frameOrderNew))
        self.addTextOrderCancel.clicked.connect(lambda : UIFunctions.countFrameText(self,self.frameOrderCancel_obj,self.frameOrderCancel))
        self.addTextOrderReady.clicked.connect(lambda : UIFunctions.countFrameText(self,self.frameOrderReady_obj,self.frameOrderReady))
        self.addTextOrderSuccess.clicked.connect(lambda : UIFunctions.countFrameText(self,self.frameOrderSuccess_obj,self.frameOrderSuccess))
        self.addTextOrderShipping.clicked.connect(lambda : UIFunctions.countFrameText(self,self.frameOrderShipping_obj,self.frameOrderShipping))

        self.addTextOrderNew.clicked.connect(lambda : ChatBot.unSaveChatBot(self))
        self.addTextOrderCancel.clicked.connect(lambda : ChatBot.unSaveChatBot(self))
        self.addTextOrderReady.clicked.connect(lambda : ChatBot.unSaveChatBot(self))
        self.addTextOrderSuccess.clicked.connect(lambda : ChatBot.unSaveChatBot(self))
        self.addTextOrderShipping.clicked.connect(lambda : ChatBot.unSaveChatBot(self))

        self.addTextOneStar.clicked.connect(lambda : UIFunctions.countFrameText(self,self.frameOneStar_obj,self.frameOneStar))
        self.addTextTwoStar.clicked.connect(lambda : UIFunctions.countFrameText(self,self.frameTwoStar_obj,self.frameTwoStar))
        self.addTextThreeStar.clicked.connect(lambda : UIFunctions.countFrameText(self,self.frameThreeStar_obj,self.frameThreeStar))
        self.addTextFourStar.clicked.connect(lambda : UIFunctions.countFrameText(self,self.frameFourStar_obj,self.frameFourStar))
        self.addTextFiveStar.clicked.connect(lambda : UIFunctions.countFrameText(self,self.frameFiveStar_obj,self.frameFiveStar))
        
        self.addTextOneStar.clicked.connect(lambda : ReplyRating.unSaveReplyRating(self))
        self.addTextTwoStar.clicked.connect(lambda : ReplyRating.unSaveReplyRating(self))
        self.addTextThreeStar.clicked.connect(lambda : ReplyRating.unSaveReplyRating(self))
        self.addTextFourStar.clicked.connect(lambda : ReplyRating.unSaveReplyRating(self))
        self.addTextFiveStar.clicked.connect(lambda : ReplyRating.unSaveReplyRating(self))        


        # ########################################################################
        ## FIRST LAUNCH APP - START FUNCTION FOR UPDATE DATA MAIN WINDOW
        # ########################################################################
        

        QTimer.singleShot(100, lambda: UserShopee.setDataUserShopee(self))
        UserShopee.setComboBoxUser(self)
        UIFunctions.setActiveFunctions(self)
        # QTimer.singleShot(100, lambda: UIFunctions.set_data_rating_shopee(self))
        QTimer.singleShot(100, lambda: ProductPush.setDataProductPush(self))
        QTimer.singleShot(100, lambda: ChatBot.setChatBotPlainText(self))
        QTimer.singleShot(100, lambda: ReplyRating.setReplyRatingPlainText(self))
        QTimer.singleShot(100, lambda: UIFunctions.openBrowser(self))

        # ########################################################################
        ## SETUP QTHREAD
        # ########################################################################


        QTimer.singleShot(100, lambda: UIFunctions.runReplyReviews(self))
        QTimer.singleShot(100, lambda: UIFunctions.runPushProduct(self))


        # ########################################################################
        ## SETUP SIGNAL BUTTON
        # ########################################################################

        self.btn_add_product_push.clicked.connect(lambda: ProductPush.popupAddProductPush(self))
     
        Dashboard.comboBox_user_text = self.comboBox_user.currentText()

        # ########################################################################
        ## BUTTON SIGNAL CHAT BOT
        # ########################################################################

        self.btnOrderNew.clicked.connect(lambda: ChatBot.btnChatBot(self))
        self.btnOrderReady.clicked.connect(lambda: ChatBot.btnChatBot(self))
        self.btnOrderShipping.clicked.connect(lambda: ChatBot.btnChatBot(self))
        self.btnOrderSuccess.clicked.connect(lambda: ChatBot.btnChatBot(self))
        self.btnOrderCancel.clicked.connect(lambda: ChatBot.btnChatBot(self))

        self.stackedWidgetChatBot.setCurrentIndex(0)
       
        self.btnSaveOrderNew.clicked.connect(lambda: ChatBot.btnSaveChatBot(self))
        self.btnSaveOrderReady.clicked.connect(lambda: ChatBot.btnSaveChatBot(self))
        self.btnSaveOrderShipping.clicked.connect(lambda: ChatBot.btnSaveChatBot(self))
        self.btnSaveOrderSuccess.clicked.connect(lambda: ChatBot.btnSaveChatBot(self))
        self.btnSaveOrderCancel.clicked.connect(lambda: ChatBot.btnSaveChatBot(self))



        # ########################################################################
        ## BUTTON SIGNAL REPLY RATING
        # ########################################################################

        self.btnOneStar.clicked.connect(lambda: ReplyRating.btnReplyRating(self))
        self.btnTwoStar.clicked.connect(lambda: ReplyRating.btnReplyRating(self))
        self.btnThreeStar.clicked.connect(lambda: ReplyRating.btnReplyRating(self))
        self.btnFourStar.clicked.connect(lambda: ReplyRating.btnReplyRating(self))
        self.btnFiveStar.clicked.connect(lambda: ReplyRating.btnReplyRating(self))

        self.stackedWidgetReplyRating.setCurrentIndex(0)

        self.btnSaveOneStar.clicked.connect(lambda: ReplyRating.btnSaveReplyRating(self))
        self.btnSaveTwoStar.clicked.connect(lambda: ReplyRating.btnSaveReplyRating(self))
        self.btnSaveThreeStar.clicked.connect(lambda: ReplyRating.btnSaveReplyRating(self))
        self.btnSaveFourStar.clicked.connect(lambda: ReplyRating.btnSaveReplyRating(self))
        self.btnSaveFiveStar.clicked.connect(lambda: ReplyRating.btnSaveReplyRating(self))


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

    def updateLogPushProduct(self,text):
        self.writeLog(text,1,"g")

    def updateInfoPushProduct(self,index):
        with open("temp//data.json") as f:
            data = json.load(f)
        
        listPush = data['shopee'][index]['list_push_product']
        count = 0
        for product in listPush:
            if product['done'] == "False":
                count += 1
        
        if count == 0:
            for indexProduct, product in enumerate(listPush):
                data['shopee'][index]['list_push_product'][indexProduct]['done'] = "False"
                Database_mongoDB.find_and_updateDB(self,data['id_wp'],{f"shopee.{index}.list_push_product.{indexProduct}.done" : "False"})
        self.writeLog(f"Còn {count} sản phẩm có thể đẩy của Shop {data['shopee'][index]['shop_name']}",1)
        with open('temp//data.json', 'w') as f:
            json.dump(data, f)
                
    def updateInfoRealyReviews(self,k):
        self.writeLog(k,1)

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
        Dashboard.comboBox_user_text = self.comboBox_user.currentText()
        l = [self.tableWidget_product_push]
        for x in l:
            for i in reversed(range(x.rowCount())):
                x.removeRow(i)

        obj = [
            self.frameOrderNew_obj,
            self.frameOrderReady_obj,
            self.frameOrderShipping_obj,
            self.frameOrderSuccess_obj,
            self.frameOrderCancel_obj,
            self.frameOneStar_obj,
            self.frameTwoStar_obj,
            self.frameThreeStar_obj,
            self.frameFourStar_obj,
            self.frameFiveStar_obj,
            ]

        layout = [
            self.frameOrderNew,
            self.frameOrderReady,
            self.frameOrderShipping,
            self.frameOrderSuccess,
            self.frameOrderCancel,
            self.frameOneStar,
            self.frameTwoStar,
            self.frameThreeStar,
            self.frameFourStar,
            self.frameFiveStar,
            ]    
        for o , l in zip(obj, layout):
            for i in range(len(o.findChildren(QPlainTextEdit))):
                l.removeWidget(o.findChildren(QPlainTextEdit)[0])
                l.removeWidget(o.findChildren(QLabel)[0])
                l.removeWidget(o.findChildren(QLabel)[0])
                l.removeWidget(o.findChildren(QPushButton)[0])

        QTimer.singleShot(100, lambda: ProductPush.setDataProductPush(self))
        QTimer.singleShot(100, lambda: ChatBot.setChatBotPlainText(self))
        QTimer.singleShot(100, lambda: ReplyRating.setReplyRatingPlainText(self))
        QTimer.singleShot(100, lambda: UIFunctions.openBrowser(self))
        UIFunctions.setActiveFunctions(self)
 
    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def resizeEvent(self, event):
        return super(Dashboard, self).resizeEvent(event)

    def checkShopChoose(self):

        with open('temp//data.json') as f:
            data = json.load(f)
        if len(data['shopee']) != 0:
            for x in range(len(data['shopee'])):
                if data['shopee'][x]['shop_name'] == self.comboBox_user.currentText():
                    shop_choose = x
        return shop_choose



    def updateToDataJson(self,_id):
        with open('temp//data.json') as f:
            data = json.load(f)
        x = Database_mongoDB.registered_Users_Collection.find({'_id': _id})
        for y in x:
            data['shopee'] = y['shopee']
        with open('temp//data.json', 'w') as f:
            json.dump(data, f)

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
        

    def writeLog(self,textLog,w=0,style=None):
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        log = f'<b>{current_time}</b> - {textLog}'
        if style == "r":
            log = f'<span style="color:red;"><b>{current_time}</b> - {textLog}</span>'
        elif style == "g":
            log = f'<span style="color:green;"><b>{current_time}</b> - {textLog}</span>'
        if w == 0:
            self.textLogSystem.appendHtml(log)
        elif w == 1:
            self.textLogFunction.appendHtml(log)

    def Button(self):
        btnWidget = self.sender()
        
        if btnWidget.objectName() == "btn_new_user_shopee":
            self.stackedWidget.setCurrentWidget(self.page_new_user_shopee)
            UIFunctions.resetStyle(self, "btn_new_user_shopee")
            UIFunctions.labelPage(self, "Tài khoản Shopee")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_reply_rating":          
            if self.comboBox_user.count() == 0 :
                r = QMessageBox.warning(self, 'MessageBox', "BẠN CHƯA THÊM TÀI KHOẢN.\nVui lòng thêm ít nhất 1 tài khoản để sử dụng", QMessageBox.Ok, QMessageBox.Ok)
            else:        
                self.stackedWidget.setCurrentWidget(self.page_reply_rating)
                UIFunctions.resetStyle(self, "btn_reply_rating")
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


        if btnWidget.objectName() == "btn_log":
            self.stackedWidget.setCurrentWidget(self.page_log)
            UIFunctions.resetStyle(self, "btn_log")
            UIFunctions.labelPage(self, "Log")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_settings":
            self.stackedWidget.setCurrentWidget(self.page_reply_rating)
            UIFunctions.resetStyle(self, "btn_settings")
            UIFunctions.labelPage(self, "Setting")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))            

class Toggle(QCheckBox):

    _transparent_pen = QPen(Qt.transparent)
    _light_grey_pen = QPen(Qt.lightGray)

    def __init__(self,
        parent=None,
        bar_color="#F7403A",
        checked_color="#4070F4",
        handle_color=Qt.white,
        ):
        super().__init__(parent)


        self._bar_brush = QBrush(QColor(bar_color))
        self._bar_checked_brush = QBrush(QColor(checked_color).lighter())

        self._handle_brush = QBrush(handle_color)
        self._handle_checked_brush = QBrush(QColor(checked_color))


        self.setContentsMargins(8, 0, 8, 0)
        self._handle_position = 0

        self.stateChanged.connect(self.handle_state_change)

    def sizeHint(self):
        return QSize(80, 60)

    def hitButton(self, pos: QPoint):
        return self.contentsRect().contains(pos)

    def paintEvent(self, e: QPaintEvent):

        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(
            0, 0,
            contRect.width() - handleRadius, 0.40 * contRect.height()
        )
        barRect.moveCenter(contRect.center())
        rounding = barRect.height() / 2

        trailLength = contRect.width() - 2 * handleRadius
        xPos = contRect.x() + handleRadius + trailLength * self._handle_position

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(
            QPointF(xPos, barRect.center().y()),
            handleRadius, handleRadius)

        p.end()

    @pyqtSlot(int)
    def handle_state_change(self, value):
        self._handle_position = 1 if value else 0

    @pyqtProperty(float)
    def handle_position(self):
        return self._handle_position

    @handle_position.setter
    def handle_position(self, pos):
        self._handle_position = pos
        self.update()

    @pyqtProperty(float)
    def pulse_radius(self):
        return self._pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos):
        self._pulse_radius = pos
        self.update()
