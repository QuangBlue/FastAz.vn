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

from data_example import *
  

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

        self.set_data_user_shopee()

        self.btn_save_ratting.clicked.connect(self.pop_up_ratting)


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
        

    def set_data_user_shopee(self):
        row = 0
        self.tableWidget.setRowCount(len(shopee) if len(shopee) >25 else 25)
        for data in shopee:
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
        if len(shopee) > 0:
            self.comboBox_user.removeItem(0)
            for x in range(len(shopee)):
                self.comboBox_user.addItem(shopee[x]['shop_name'])

        self.comboBox_user.currentTextChanged.connect(lambda: print(self.comboBox_user.currentText()))

    def pop_up_ratting(self):
        self.ui = Popup_Ratting()
        self.ui.show()

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


class Popup_Ratting(QMainWindow):
    def __init__(self):
        super(Popup_Ratting,self).__init__()
        loadUi("ui//popup_ratting.ui",self)

        self.btn_send.clicked.connect(self.send_info)

    def send_info(self):
        print(self.comboBox_ratting.currentText())
        x = self.plainTextEdit_ratting.toPlainText().replace("\n"," ")
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont('font/Nunito/Nunito-Regular.ttf')
    QtGui.QFontDatabase.addApplicationFont('font/Nunito/Nunito-Regular.ttf')
    dashboard = Dashboard()
    dashboard.installEventFilter(dashboard)
    app.exec_() 