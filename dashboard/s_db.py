from Dashboard import *
from browser import Browser

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
            standard = 70

            if width == 70:
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
        button.setMinimumSize(QSize(0, 70))
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
        select = getStyle + ("QPushButton { border-right: 7px solid rgb(44, 49, 60); }")
        return select

    def deselectMenu(self, getStyle):
        deselect = getStyle.replace("QPushButton { border-right: 7px solid rgb(44, 49, 60); }", "")
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

    def userIcon(self, initialsTooltip, icon, showHide):
        if showHide:
            self.label_user_icon.setText(initialsTooltip)

            if icon:
                style = self.label_user_icon.styleSheet()
                setIcon = "QLabel { background-image: " + icon + "; }"
                self.label_user_icon.setStyleSheet(style + setIcon)
                self.label_user_icon.setText('')
                self.label_user_icon.setToolTip(initialsTooltip)
        else:
            self.label_user_icon.hide()

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
        self.btn_close.clicked.connect(lambda: self.close())

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
        padding-left: 45px;
    }
    QPushButton[Active=true] {
        background-image: ICON_REPLACE;
        background-position: left center;
        background-repeat: no-repeat;
        border: none;
        border-left: 28px solid rgb(27, 29, 35);
        border-right: 5px solid rgb(44, 49, 60);
        background-color: rgb(27, 29, 35);
        text-align: left;
        padding-left: 45px;
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