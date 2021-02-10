import sys,requests,pickle
from PyQt5.QtCore import QUrl, QByteArray, QSize, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from PyQt5.QtGui import QFont
from http.cookies import SimpleCookie
from backend.MongoDB_Setup import Database_mongoDB
from backend.networks import Network
import json

class Browser(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.box = QVBoxLayout(self)
        self.btn_get = QPushButton('THÊM TÀI KHOẢN')
        self.btn_get.clicked.connect(self.get_cookie)
        self.btn_get.setObjectName(u"btn_get")
        self.btn_get.setMinimumSize(QSize(0, 40))
        self.btn_get.setStyleSheet(u"#btn_get{border-radius: 20px;padding:8px 25px 7px 25px;background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(89, 64, 231, 255), stop:1 rgba(15, 181, 253, 255));color: rgb(255, 255, 255);}#btn_get:hover{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(15, 181, 253, 255), stop:1 rgba(89, 64, 231, 255));}#btn_get:pressed{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(89, 64, 231, 255), stop:1 rgba(15, 181, 253, 255));}")
        font = QFont()
        font.setFamily(u"Nunito")
        font.setPointSize(18)
        font.setBold(True)
        self.btn_get.setFont(font)
        self.label_browser = QLabel('Sau khi đăng nhập THÀNH CÔNG vui lòng bấm vào nút THÊM TÀI KHOẢN phía trên')
        self.label_browser.setObjectName(u"label")
        self.label_browser.setMaximumSize(QSize(16777215, 40))
        font1 = QFont()
        font1.setFamily(u"Nunito")
        font1.setPointSize(16)
        font1.setBold(True)
        self.label_browser.setFont(font1)
        self.label_browser.setStyleSheet(u"color: rgb(27, 63, 216);")
        self.label_browser.setAlignment(Qt.AlignCenter)

        self.web = MyWebEngineView()
        self.web.resize(1280, 720)
        self.web.load(QUrl("https://banhang.shopee.vn/"))
        self.box.addWidget(self.btn_get)
        self.box.addWidget(self.label_browser)
        self.box.addWidget(self.web)
        self.web.show()

    def get_cookie(self):
        cookie = self.web.get_cookie()
        shopee_info_json = Network.get_info_account_shopee(self,cookie)
        print(shopee_info_json)
        with open("temp//data.json") as json_file:  #Get username_az
            data = json.load(json_file)
        # Check for duplicates shopee id_sp on mongodb, if not, create a new shop with blank info.
        if not Database_mongoDB.check_shopee_username(self,data['username_az'],shopee_info_json['shopid']):
            Database_mongoDB.insert_new_shopee_mongodb(self,data['username_az'],cookie,shopee_info_json['id'],shopee_info_json['shopid'],shopee_info_json['username'])
            #Tạo pop up message nếu thành công
        else:
            #Tạo pop up message không thành công
            print("Shop này đã có trên database")
        self.close()

class MyWebEngineView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super(MyWebEngineView, self).__init__(*args, **kwargs)

        QWebEngineProfile.defaultProfile().cookieStore().deleteAllCookies()
        QWebEngineProfile.defaultProfile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}

    def onCookieAdd(self, cookie):
        name = cookie.name().data().decode('utf-8')
        value = cookie.value().data().decode('utf-8')
        self.cookies[name] = value


    def get_cookie(self):
        return self.cookies


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Browser()
    w.show()
    sys.exit(app.exec_())
