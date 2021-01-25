import sys
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.uic import loadUi
import qrc.file_img_rc
import webbrowser
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
sys.path.insert(0, 'dashboard/')
from s_db import *
  

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
        UIFunctions.addNewMenu(self, "Open File", "btn_open_file", "url(:/icon/cil-folder-open.png)", True)
        UIFunctions.addNewMenu(self, "Save", "btn_save", "url(:/icon/cil-save.png)", True)
        UIFunctions.addNewMenu(self, "New", "btn_new", "url(:/icon/cil-file.png)", True)
        UIFunctions.addNewMenu(self, "Setting", "btn_settings", "url(:/icon/cil-settings.png)", False)




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
        ## LỰA CHỌN MENU MẶC ĐỊNH
        # ########################################################################
        
        UIFunctions.selectStandardMenu(self, "btn_new_user_shopee")
        self.stackedWidget.setCurrentWidget(self.page_home)

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

        if btnWidget.objectName() == "btn_open_file":
            self.stackedWidget.setCurrentWidget(self.page_home)
            UIFunctions.resetStyle(self, "btn_open_file")
            UIFunctions.labelPage(self, "Open File")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_save":
            self.stackedWidget.setCurrentWidget(self.page_home)
            UIFunctions.resetStyle(self, "btn_save")
            UIFunctions.labelPage(self, "Save")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self, btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_new":
            self.stackedWidget.setCurrentWidget(self.page_home)
            UIFunctions.resetStyle(self, "btn_new")
            UIFunctions.labelPage(self, "New")
            btnWidget.setStyleSheet(UIFunctions.selectMenu(self,btnWidget.styleSheet()))

        if btnWidget.objectName() == "btn_new_user_shopee":
            self.stackedWidget.setCurrentWidget(self.page_home)
            UIFunctions.resetStyle(self, "btn_new_user")
            UIFunctions.labelPage(self, "Tài khoản Shopee")
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