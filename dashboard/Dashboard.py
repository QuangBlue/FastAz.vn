from main_pyqt5 import *
from dashboard.s_db import *
from dashboard.style import *
from dashboard.browser import Browser
from data_example import *
from backend.MongoDB_Setup import * 

status_user = 1
status_rating = 1

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
        UIFunctions.addNewMenu(self, "Setting", "btn_settings", "url(:/icon/cil-settings.png)", False)


        # ########################################################################
        ## SHOPEE SHOW-OFF
        # ########################################################################

        # ########################################################################
        ## FIRST LAUNCH APP - START FUNCTION FOR UPDATE DATA MAIN WINDOW
        # ########################################################################


        QTimer.singleShot(100, lambda: UIFunctions.set_data_user_shopee(self))
        UIFunctions.set_comboBox_user(self)
        QTimer.singleShot(100, lambda: UIFunctions.set_data_rating_shopee(self))
        QTimer.singleShot(100, lambda: UIFunctions.set_data_product_push(self))
        QTimer.singleShot(100, lambda: UIFunctions.get_list_products_shopee(self))


        # ########################################################################
        ## SETUP SIGNAL BUTTON
        # ########################################################################


        self.btn_add.clicked.connect(lambda: UIFunctions.add_to_product_push(self))
        self.btn_remove.clicked.connect(lambda: UIFunctions.del_from_product_push(self))
        
        self.btn_forward.clicked.connect(lambda : UIFunctions.next_page(self))
        self.btn_back.clicked.connect(lambda : UIFunctions.back_page(self))
        
        self.btn_add_rating.clicked.connect(lambda: UIFunctions.pop_up_rating(self))
        self.btn_apply_all_rating.clicked.connect(lambda: UIFunctions.set_data_rating_shopee(self))
        
        Dashboard.comboBox_user_text = self.comboBox_user.currentText()


        # ########################################################################
        ## BUTTON CHANGE THEME
        # ########################################################################

        self.btn_theme.clicked.connect(lambda: UIFunctions.change_theme(self))

        # ########################################################################
        ## SETUP NEW THREAD FOR UPDATE ACCOUNT SHOPEE INFO
        # ########################################################################

        self.threadgetinfo = ThreadGetInfo()
        self.threadgetinfo.start()
        self.threadgetinfo.finished.connect(lambda: UIFunctions.set_data_user_shopee(self))


        # ########################################################################
        ## SET UPDATE WHEN COMBOX CHANGE
        # ########################################################################
        self.comboBox_user.currentIndexChanged.connect(lambda: self.change_comboBox() )


        # ########################################################################
        ## ONLY SELECT TABLE ROW SAME TIME
        # ########################################################################

        self.product_list_shopee.selectionModel().selectionChanged.connect(lambda: self.product_list_user.clearSelection())
        self.product_list_user.selectionModel().selectionChanged.connect(lambda: self.product_list_shopee.clearSelection())


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

        self.btn_add_user.clicked.connect(lambda: UIFunctions.open_browser(self))

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
            self.product_list_user.setCellWidget(l[0],0,imgLabel)

 
    def change_comboBox(self):
        Dashboard.comboBox_user_text = self.comboBox_user.currentText()
        l = [ self.tw_ratting1, self.tw_ratting1,self.tw_ratting3,self.tw_ratting4,self.tw_ratting5,self.product_list_shopee,self.product_list_user]
        for x in l:
            for i in reversed(range(x.rowCount())):
                x.removeRow(i)
        QTimer.singleShot(100, lambda: UIFunctions.set_data_rating_shopee(self))
        QTimer.singleShot(100, lambda: UIFunctions.set_data_product_push(self))
        QTimer.singleShot(100, lambda:UIFunctions.get_list_products_shopee(self))
 
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
            if self.comboBox_user.count() == 0 or self.comboBox_user.currentText() == "Chưa có tài khoản":
                r = QMessageBox.warning(self, 'MessageBox', "BẠN CHƯA THÊM TÀI KHOẢN.\nVui lòng thêm ít nhất 1 tài khoản để sử dụng", QMessageBox.Ok, QMessageBox.Ok)
            else:        
                self.stackedWidget.setCurrentWidget(self.page_reply_ratting)
                UIFunctions.resetStyle(self, "btn_reply_ratting")
                UIFunctions.labelPage(self, "Trả lời Đánh giá")
                btnWidget.setStyleSheet(UIFunctions.selectMenu(self, btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_push_product":
            if self.comboBox_user.count() == 0 or self.comboBox_user.currentText() == "Chưa có tài khoản":
                r = QMessageBox.warning(self, 'MessageBox', "BẠN CHƯA THÊM TÀI KHOẢN.\nVui lòng thêm ít nhất 1 tài khoản để sử dụng", QMessageBox.Ok, QMessageBox.Ok)
            else: 
                
                self.stackedWidget.setCurrentWidget(self.page_push_product)
                UIFunctions.resetStyle(self, "btn_push_product")
                UIFunctions.labelPage(self, "Đẩy sản phẩm")
                btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))

                
                
        if btnWidget.objectName() == "btn_chat_bot":
            if self.comboBox_user.count() == 0 or self.comboBox_user.currentText() == "Chưa có tài khoản":
                r = QMessageBox.warning(self, 'MessageBox', "BẠN CHƯA THÊM TÀI KHOẢN.\nVui lòng thêm ít nhất 1 tài khoản để sử dụng", QMessageBox.Ok, QMessageBox.Ok)
            else:
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
         

