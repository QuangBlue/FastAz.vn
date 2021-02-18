from main_pyqt5 import *
from dashboard.s_db import *
from dashboard.browser import Browser
from data_example import *
from backend.MongoDB_Setup import * 

status_user = 1
status_rating = 1

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

        UIFunctions.set_data_user_shopee(self)
        UIFunctions.set_data_rating_shopee(self)
        self.comboBox_user.currentTextChanged.connect(lambda: UIFunctions.set_data_rating_shopee(self))
        self.btn_add_rating.clicked.connect(lambda: UIFunctions.pop_up_rating(self))
        self.btn_apply_all_rating.clicked.connect(lambda: UIFunctions.set_data_rating_shopee(self))


        Dashboard.comboBox_user_text = self.comboBox_user.currentText()

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

        

