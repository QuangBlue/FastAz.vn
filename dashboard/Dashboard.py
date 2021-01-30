import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
import qrc.file_img_rc
import webbrowser
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from dashboard.s_db import *
from dashboard.browser import Browser
  

class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard,self).__init__()
        loadUi("ui//dashboard_screen.ui",self)
        self.resize(1920, 1080)
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
        ## HIỂN THỊ DANH SÁCH TÀI KHOẢN SHOPEE
        # ########################################################################

        data_example = [

            {"id_sp" : "123456", "shop_name" : "Naxa Shop", "shop_id" : "456456456", "total_product" : "354" ,"total_order" : "345","status_cookie" : True},
            {"id_sp" : "234234", "shop_name" : "Chuột May Mắn", "shop_id" : "34343434", "total_product" : "234" ,"total_order" : "6565", "status_cookie" : True},
            {"id_sp" : "456456", "shop_name" : "Fortune Mouse", "shop_id" : "67868678", "total_product" : "367" ,"total_order" : "4676", "status_cookie" : True},
            {"id_sp" : "434663", "shop_name" : "Quang Shop", "shop_id" : "446565767", "total_product" : "4546" ,"total_order" : "2356", "status_cookie" : True},
            {"id_sp" : "565656", "shop_name" : "Huy Shop", "shop_id" : "34545454", "total_product" : "676" ,"total_order" : "787", "status_cookie" : False},
            {"id_sp" : "343436", "shop_name" : "Quang Huy Shop", "shop_id" : "5657556", "total_product" : "334" ,"total_order" : "7875", "status_cookie" : False}

            ]

        # btn_giahan= QPushButton(self.tableWidget)
        # btn_giahan.setText('Gia Hạn')
        # self.tableWidget.setCellWidget(5,5,btn_giahan)
        row = 0
        self.tableWidget.setRowCount(len(data_example) if len(data_example) >25 else 25)
        for data in data_example:
            self.tableWidget.setItem(row, 0,QtWidgets.QTableWidgetItem(data['id_sp']))
            self.tableWidget.setItem(row, 1,QtWidgets.QTableWidgetItem(data['shop_name']))
            self.tableWidget.setItem(row, 2,QtWidgets.QTableWidgetItem(data['shop_id']))
            self.tableWidget.setItem(row, 3,QtWidgets.QTableWidgetItem(data['total_product']))
            self.tableWidget.setItem(row, 4,QtWidgets.QTableWidgetItem(data['total_order']))
            self.tableWidget.setItem(row, 5,QtWidgets.QTableWidgetItem('Còn Hiệu Lực') if data['status_cookie'] == True else QtWidgets.QTableWidgetItem('Hết Hiệu Lực'))
            self.tableWidget.item(row, 5).setForeground(QtGui.QColor(73, 165, 43) if data['status_cookie'] == True else QtGui.QColor(201, 5, 22))
            font = QtGui.QFont()
            font.setBold(True)
            self.tableWidget.item(row, 5).setFont(font)
            row = row + 1
        if len(data_example) > 0:
            self.comboBox_user.removeItem(0)
            for x in range(len(data_example)):
                self.comboBox_user.addItem(data_example[x]['shop_name'])

        self.comboBox_user.currentTextChanged.connect(lambda: print(self.comboBox_user.currentText()))



        # ########################################################################
        ## ICON HOẶC AVARTA CỦA USER
        # ########################################################################

        UIFunctions.userIcon(self, "QH", "", True)
        self.label_user_icon.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.label_user_icon.customContextMenuRequested.connect(lambda pos, child=self.label_user_icon: self.customMenuEvent(pos, child))
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

    def customMenuEvent(self, eventPosition, child):
        child = self.childAt(self.sender().mapTo(self, eventPosition))
        contextMenu = QMenu(self)
        getText = contextMenu.addAction("Text")
        getName = contextMenu.addAction("Name")
        quitAct = contextMenu.addAction("Quit")
        action = contextMenu.exec_(child.mapToGlobal(eventPosition))


        if action == quitAct:
            self.close()

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
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('font/Nunito/Nunito-Regular.ttf')
    QtGui.QFontDatabase.addApplicationFont('font/Nunito/Nunito-Regular.ttf')
    dashboard = Dashboard()
    dashboard.installEventFilter(dashboard)
    app.exec_() 