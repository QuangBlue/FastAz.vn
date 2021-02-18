from dashboard.dashboard import *
from dashboard.browser import Browser
from backend.MongoDB_Setup import Database_mongoDB

GLOBAL_STATE = 0
GLOBAL_TITLE_BAR = True

count = 1

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
            self.btn_maximize_restore.setIcon(QtGui.QIcon(u":/icon/cil-window-restore.png"))
            self.frame_size_grip.hide()
        else:
            GLOBAL_STATE = 0
            self.showNormal()
            self.resize(self.width()+1, self.height()+1)
            self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.btn_maximize_restore.setToolTip("Maximize")
            self.btn_maximize_restore.setIcon(QtGui.QIcon(u":/icon/cil-window-maximize.png"))
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
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def addNewMenu(self, name, objName, icon, isTopMenu):
        font = QFont()
        font.setFamily(u"Nunito")
        font.setPointSize(16)
        button = QPushButton(str(count),self)
        button.setObjectName(objName)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(button.sizePolicy().hasHeightForWidth())
        button.setSizePolicy(sizePolicy3)
        button.setMinimumSize(QSize(0, 75))
        button.setLayoutDirection(Qt.LeftToRight)
        button.setFont(font)
        button.setStyleSheet(Style.style_bt_standard.replace('ICON_REPLACE', icon))
        button.setText(name)
        button.setToolTip(name)
        button.clicked.connect(self.Button)

        if isTopMenu:
            self.layout_menus.addWidget(button)
        else:
            self.layout_menu_bottom.addWidget(button)

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

    def userIcon(self, initialsTooltip, icon = 'url(img//teamwork.png)', showHide = True):
        if showHide:
            self.label_user_icon.setText(initialsTooltip)

            if icon:
                style = self.label_user_icon.styleSheet()
                setIcon = "QLabel { border-image: " + icon + "; }"
                self.label_user_icon.setStyleSheet(style + setIcon)
                self.label_user_icon.setText('')
                self.label_user_icon.setToolTip(initialsTooltip)
        else:
            self.label_user_icon.hide()

    def set_data_user_shopee(self):
        with open('temp//data.json') as f:
            data = json.load(f)
            shopee = data['shopee']
        row = 0
        self.tableWidget.setRowCount(len(shopee) if len(shopee) >25 else 25)
        if len(shopee) != 0: 
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
            
    def set_data_rating_shopee(self):
        with open('temp//data.json') as f:
            data = json.load(f)
            shopee = data['shopee']
        shop_c = 0
        if len(shopee) != 0: 
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
                self.btn_delete1.clicked.connect(lambda: UIFunctions.delete1(self))
                self.tw_ratting1.setCellWidget(row,0,self.btn_delete1)
                self.btn_delete1.setStyleSheet('QPushButton { image: url(img//remove.png);}QPushButton:hover { image: url(img//remove_red.png);}')
                row = row + 1
            row = 0
            for data_2 in s2:                   
                self.tw_ratting2.setItem(row, 1,QtWidgets.QTableWidgetItem(str(row+1)))
                self.tw_ratting2.setItem(row, 2,QtWidgets.QTableWidgetItem(data_2))
                self.btn_delete2 = QPushButton('')
                self.btn_delete2.clicked.connect(lambda: UIFunctions.delete2(self))
                self.tw_ratting2.setCellWidget(row,0,self.btn_delete2)
                self.btn_delete2.setStyleSheet('QPushButton { image: url(img//remove.png);}QPushButton:hover { image: url(img//remove_red.png);}')          
                row = row + 1
            row = 0
            for data_3 in s3:                   
                self.tw_ratting3.setItem(row, 1,QtWidgets.QTableWidgetItem(str(row+1)))
                self.tw_ratting3.setItem(row, 2,QtWidgets.QTableWidgetItem(data_3))
                self.btn_delete3 = QPushButton('')
                self.btn_delete3.clicked.connect(lambda: UIFunctions.delete3(self))
                self.tw_ratting3.setCellWidget(row,0,self.btn_delete3)
                self.btn_delete3.setStyleSheet('QPushButton { image: url(img//remove.png);}QPushButton:hover { image: url(img//remove_red.png);}')
                row = row + 1
            row = 0
            for data_4 in s4:                   
                self.tw_ratting4.setItem(row, 1,QtWidgets.QTableWidgetItem(str(row+1)))
                self.tw_ratting4.setItem(row, 2,QtWidgets.QTableWidgetItem(data_4))
                self.btn_delete4 = QPushButton('')
                self.btn_delete4.clicked.connect(lambda: UIFunctions.delete4(self))
                self.tw_ratting4.setCellWidget(row,0,self.btn_delete4)
                self.btn_delete4.setStyleSheet('QPushButton { image: url(img//remove.png);}QPushButton:hover { image: url(img//remove_red.png);}')
                row = row + 1
            row = 0
            for data_5 in s5:                   
                self.tw_ratting5.setItem(row, 1,QtWidgets.QTableWidgetItem(str(row+1)))
                self.tw_ratting5.setItem(row, 2,QtWidgets.QTableWidgetItem(data_5))
                self.btn_delete5 = QPushButton('')
                self.btn_delete5.clicked.connect(lambda: UIFunctions.delete5(self))
                self.tw_ratting5.setCellWidget(row,0,self.btn_delete5)
                self.btn_delete5.setStyleSheet('QPushButton { image: url(img//remove.png);}QPushButton:hover { image: url(img//remove_red.png);}')
                row = row + 1
                
    def pop_up_rating(self):
        from dashboard.dashboard import Popup_Rating
        self.ui = Popup_Rating()
        self.ui.show()
        self.ui.btn_send.clicked.connect(lambda: UIFunctions.set_data_rating_shopee(self))

    def delete1(self):
        self.pos_table = self.tw_ratting1
        self.table_name = 'rating_1star'
        UIFunctions.delete_ratings(self)

    def delete2(self):
        self.pos_table = self.tw_ratting2
        self.table_name = 'rating_2star'
        UIFunctions.delete_ratings(self)

    def delete3(self):
        self.pos_table = self.tw_ratting3
        self.table_name = 'rating_3star'
        UIFunctions.delete_ratings(self)        

    def delete4(self):
        self.pos_table = self.tw_ratting4
        self.table_name = 'rating_4star'
        UIFunctions.delete_ratings(self)

    def delete5(self):
        self.pos_table = self.tw_ratting5
        self.table_name = 'rating_5star'
        UIFunctions.delete_ratings(self)

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
        UIFunctions.set_data_rating_shopee(self)    


    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QtCore.QEvent.MouseButtonDblClick:
                QtCore.QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        ## REMOVE ==> STANDARD TITLE BAR
        if GLOBAL_TITLE_BAR:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
            self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
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

    style_bt_standard = (
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
