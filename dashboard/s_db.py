from dashboard.dashboard import *
from dashboard.style import *
from dashboard.browser import Browser
from backend.MongoDB_Setup import Database_mongoDB


GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True

count = 1
page_number = 1

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
        self.label_user_icon.clicked.connect(lambda: UIFunctions.showPopupUser(self))

    def showPopupUser(self):
        msg = QMessageBox()
        msg.setWindowTitle('Thông tin tài khoản')
        msg.setText('Tài khoản của bạn là <strong>VIP 1</strong> \n Còn thời hạn đến 16/03/2022')
        logout_btn = msg.addButton('Đăng Xuất' , QMessageBox.RejectRole)
        logout_btn.clicked.connect(lambda: UIFunctions.logoutScreen(self))
        extend_vip = msg.addButton('Gia Hạn' , QMessageBox.YesRole)
        extend_vip.clicked.connect(lambda: UIFunctions.open_webbrowser(self))
        msg.exec_()
        
    def logoutScreen(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        data['savepass'] = "False"
        with open('temp//data.json', 'w') as f:
            json.dump(data, f)
        MainWindow()
        self.close()

    def open_webbrowser(self):
        webbrowser.open('http://fastaz.vn/')

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
        self.writeLog('Đổi giao diện')

    def check_theme(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        if data['theme'] == 'dark':
            self.frame_main.setStyleSheet(Style.main_dark)
            self.btn_theme.setText('Light Theme')
        elif data['theme'] == 'light':
            self.frame_main.setStyleSheet(Style.main_light)
            self.btn_theme.setText('Dark Theme')

    def openBrowser(self):
        # if len(self.page_browser.findChildren(QWebEngineView)) > 0 :
        #     for i in self.page_browser.findChildren(QWebEngineView):
        #         i.close()
        # with open('temp//data.json') as f:
        #     data = json.load(f)
        # shop_choose = self.checkShopChoose()  
        # if len(data['shopee']) != 0:
        #     def btnBrowserHome(): 
        #         self.webEngineView.setUrl(QUrl("https://banhang.shopee.vn")) 
        #     def updateUrlBar(q): 
        #         self.urlBar.setText(q.toString()) 
        #     self.webEngineView = MyWebView(data['shopee'][shop_choose]['pathName'])
        #     self.layoutBrowers.addWidget(self.webEngineView)
        #     self.urlBar.setText("https://banhang.shopee.vn")
        #     self.webEngineView.urlChanged.connect(updateUrlBar) 
        #     self.browserBack.clicked.connect(self.webEngineView.back) 
        #     self.browserForward.clicked.connect(self.webEngineView.forward)
        #     self.browserReload.clicked.connect(self.webEngineView.reload) 
        #     self.browserHome.clicked.connect(btnBrowserHome)
        #     # self.openBrowser.clicked.connect()
        #     self.webEngineView.show()
        #     self.writeLog(f"Mở browser với profile {data['shopee'][shop_choose]['pathName']}")
        pass
    def countFrameText(self,obj,layout):
        r = obj.findChildren(QPlainTextEdit)
        UIFunctions.addFrameText(self,len(r)+1,obj,layout)

    def addFrameText(self,count,obj,layout,text='',lenText=0):
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
        plainText.setPlaceholderText('Nội dung sẽ gửi cho khách hàng.')
        plainText.setFocus()
        plainText.setPlainText(text)

        sizePolicy2 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)

        label = QLabel(f"{count}#")
        label.setObjectName(f"label_{count}")
        label.setFont(font)
        label.setSizePolicy(sizePolicy2)

        font1 = QFont()
        font1.setFamily(u"Nunito")
        font1.setPointSize(14)


        labelCount = QLabel(f"{lenText}/400")
        labelCount.setObjectName(f"count_{count}")
        labelCount.setFont(font1)
        labelCount.setStyleSheet("color : #A6A6A6")
        
        plainText.textChanged.connect(lambda : UIFunctions.countPlainTextEdit(self,obj,layout))

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
        frameT.addWidget(labelCount)
        frameT.addWidget(btn)
        layout.addLayout(frameT)
        layout.addWidget(plainText)

    def countPlainTextEdit(self,obj,layout):
        widget = self.sender()
        objNameCountText = widget.objectName()
        objNameCountLabel = objNameCountText.replace("plainText","count")
        plainTextCount = obj.findChildren(QPlainTextEdit,objNameCountText)[0]
        labelCountText = obj.findChildren(QLabel,objNameCountLabel)[0]
        countText = len(plainTextCount.toPlainText())
        labelCountText.setText(f"{countText}/400")

        if countText > 400:
            labelCountText.setStyleSheet("color : red")
            plainTextCount.setStyleSheet("border: 1px solid red;")     
        else:
            labelCountText.setStyleSheet("color : #A6A6A6")
            plainTextCount.setStyleSheet("border: 1px solid rgb(127, 126, 128);")
        


    def delPlainTextEdit(self,obj,layout):
        btnWidget = self.sender()
        objName = btnWidget.objectName()
        layout.removeWidget(obj.findChildren(QLabel , f'label{objName}')[0]) 
        layout.removeWidget(obj.findChildren(QPushButton, f'{objName}')[0])
        layout.removeWidget(obj.findChildren(QPlainTextEdit, f'plainText{objName}')[0])
        layout.removeWidget(obj.findChildren(QLabel, f'count{objName}')[0])
        self.writeLog('Xóa nội dụng chat bot')

        if layout in [self.frameOrderNew,
            self.frameOrderReady,
            self.frameOrderShipping,
            self.frameOrderSuccess,
            self.frameOrderCancel]:
            self.btnSaveOrderNew.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.btnSaveOrderReady.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.btnSaveOrderShipping.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.btnSaveOrderSuccess.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.btnSaveOrderCancel.setStyleSheet('background-color: rgb(217, 38, 0);')
        elif layout in [self.frameOneStar,
            self.frameTwoStar,
            self.frameThreeStar,
            self.frameFourStar,
            self.frameFiveStar]:
            self.btnSaveOneStar.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.btnSaveTwoStar.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.btnSaveThreeStar.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.btnSaveFourStar.setStyleSheet('background-color: rgb(217, 38, 0);')
            self.btnSaveFiveStar.setStyleSheet('background-color: rgb(217, 38, 0);')

    def runThreadReplyReviews(self,accShopee):
        self.writeLog(f"Chạy đánh giá Shop {accShopee['shop_name']}",1)
        self.workerRealyReviews[accShopee['shop_name']] = ThreadReplyReviews(accShopee)
        self.workerRealyReviews[accShopee['shop_name']].start()
        self.workerRealyReviews[accShopee['shop_name']].update_k.connect(self.updateInfoRealyReviews)

    def stopThreadReplyReviews(self,accShopee):
        self.writeLog(f"Ngưng chạy đánh giá Shop {accShopee['shop_name']}",1)
        self.workerRealyReviews[accShopee['shop_name']].quit()

    def checkThreadReplyReviews(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        shop_choose = self.checkShopChoose()
        accShopee = data['shopee'][shop_choose]
        if self.btnReplyRatingSwitch.isChecked() == True:
            UIFunctions.runThreadReplyReviews(self,accShopee)
        elif self.btnReplyRatingSwitch.isChecked() == False:
            UIFunctions.stopThreadReplyReviews(self,accShopee)

    def runReplyReviews(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        for index, accShopee in enumerate(data['shopee']):
            listActiveFunctions = accShopee['active_functions']
            if 'replyRatingSwitch' in listActiveFunctions:
                UIFunctions.runThreadReplyReviews(self,accShopee)

    def runThreadPushProduct(self,accShopee,index):
        self.writeLog(f"Chạy đẩy sản phẩm Shop {accShopee['shop_name']}",1)
        self.workerPushProduct[accShopee['shop_name']] = ThreadPushProducts(accShopee,index)
        self.workerPushProduct[accShopee['shop_name']].start()
        self.workerPushProduct[accShopee['shop_name']].donePushProduct.connect(self.updateInfoPushProduct)
        self.workerPushProduct[accShopee['shop_name']].pushProductText.connect(self.updateLogPushProduct)

    def stopThreadPushProduct(self,accShopee):
        self.writeLog(f"Ngưng chạy đẩy sản phẩm Shop {accShopee['shop_name']}",1)
        self.workerPushProduct[accShopee['shop_name']].quit()

    def checkThreadPushProduct(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        shop_choose = self.checkShopChoose()
        accShopee = data['shopee'][shop_choose]
        if self.btnPushProductSwitch.isChecked() == True:
            UIFunctions.runThreadPushProduct(self,accShopee,shop_choose)
        elif self.btnPushProductSwitch.isChecked() == False:
            UIFunctions.stopThreadPushProduct(self,accShopee)

    def runPushProduct(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        for index, accShopee in enumerate(data['shopee']):
            listActiveFunctions = accShopee['active_functions']
            if 'pushProductSwitch' in listActiveFunctions:
                UIFunctions.runThreadPushProduct(self,accShopee,index)

    def setActiveFunctions(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        shop_choose = self.checkShopChoose()
        self.btnPushProductSwitch.setChecked(False)
        self.btnReplyRatingSwitch.setChecked(False)
        self.btnChatBotSwitch.setChecked(False)
        listFunctions = data['shopee'][shop_choose]['active_functions']

        for x in listFunctions:
            if x == "pushProductSwitch":
                self.btnPushProductSwitch.setChecked(True)
            elif x == "replyRatingSwitch":
                self.btnReplyRatingSwitch.setChecked(True)
            elif x == "chatBotSwitch":
                self.btnChatBotSwitch.setChecked(True)

    def setSwitchEnable(self):
        with open('temp//data.json') as f:
            data = json.load(f)
        shop_choose = self.checkShopChoose()
        btn = self.sender()
        objName = btn.objectName()
        
        if objName == 'pushProductSwitch':
            if  (
                len(data['shopee'][shop_choose]['list_push_product']) != 0 
                ):
                UIFunctions.activeFunctions(self,self.btnPushProductSwitch.isChecked(),objName)
                UIFunctions.checkThreadPushProduct(self)
            else:
                self.btnPushProductSwitch.setChecked(False)
                QMessageBox.warning(self, 'Cảnh báo', "Vui lòng thêm ít nhất 1 sản phẩm đẩy để có thể kích hoạt Đẩy Sản Phẩm", QMessageBox.Ok)

        elif objName == "replyRatingSwitch":
            try:
                if (
                    len(data['shopee'][shop_choose]['replyRatingList']['1']) != 0 or
                    len(data['shopee'][shop_choose]['replyRatingList']['2']) != 0 or
                    len(data['shopee'][shop_choose]['replyRatingList']['3']) != 0 or
                    len(data['shopee'][shop_choose]['replyRatingList']['4']) != 0 or
                    len(data['shopee'][shop_choose]['replyRatingList']['5']) != 0               
                    ):
                    UIFunctions.activeFunctions(self,self.btnReplyRatingSwitch.isChecked(),objName)
                    UIFunctions.checkThreadReplyReviews(self)
                        
                else:
                    self.btnReplyRatingSwitch.setChecked(False)
                    QMessageBox.warning(self, 'Cảnh báo', "Vui lòng thêm ít nhất 1 đánh giá để có thể kích hoạt Đánh Giá", QMessageBox.Ok)
            except:
                self.btnReplyRatingSwitch.setChecked(False)
                QMessageBox.warning(self, 'Cảnh báo', "Vui lòng thêm ít nhất 1 đánh giá để có thể kích hoạt Đánh Giá", QMessageBox.Ok)
        elif objName == "chatBotSwitch":
            try:
                if (
                    len(data['shopee'][shop_choose]['orderChatBotList']['textOrderCancel']) != 0 or
                    len(data['shopee'][shop_choose]['orderChatBotList']['textOrderNew']) != 0 or
                    len(data['shopee'][shop_choose]['orderChatBotList']['textOrderReady']) != 0 or
                    len(data['shopee'][shop_choose]['orderChatBotList']['textOrderShipping']) != 0 or
                    len(data['shopee'][shop_choose]['orderChatBotList']['textOrderSuccess']) != 0               
                    ):
                    UIFunctions.activeFunctions(self,self.btnChatBotSwitch.isChecked(),objName)
                else:
                    self.btnChatBotSwitch.setChecked(False)
                    QMessageBox.warning(self, 'Cảnh báo', "Vui lòng thêm ít nhất 1 câu trả lời để có thể kích hoạt ChatBot", QMessageBox.Ok)
            except:
                self.btnChatBotSwitch.setChecked(False)
                QMessageBox.warning(self, 'Cảnh báo', "Vui lòng thêm ít nhất 1 câu trả lời để có thể kích hoạt ChatBot", QMessageBox.Ok)



    def activeFunctions(self,active,objName):
        with open('temp//data.json') as f:
            data = json.load(f)
        shop_choose = self.checkShopChoose()

        listFunctions = ["pushProductSwitch","replyRatingSwitch","chatBotSwitch"]
        for x in listFunctions:
            if objName == x and active == True and objName not in data['shopee'][shop_choose]['active_functions']:
                data['shopee'][shop_choose]['active_functions'].append(objName)
                Database_mongoDB.registered_Users_Collection.replace_one({'_id':data['id_wp']},data,upsert = True)
            elif objName == x and active == False and objName in data['shopee'][shop_choose]['active_functions']:
                data['shopee'][shop_choose]['active_functions'].remove(objName)
                Database_mongoDB.registered_Users_Collection.replace_one({'_id':data['id_wp']},data,upsert = True)
            with open('temp//data.json', 'w') as f:
                json.dump(data, f)

    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(100, lambda: UIFunctions.maximize_restore(self))

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