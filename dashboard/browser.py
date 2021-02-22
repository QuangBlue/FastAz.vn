import sys,requests, json
from PyQt5.QtCore import QUrl, Qt ,QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from PyQt5.QtGui import QFont, QPixmap
from backend.MongoDB_Setup import Database_mongoDB
from backend.networks import Network
import json

status = 0

class Browser(QWidget):
    def __init__(self):
        super().__init__()
        global status
        status = 0
        self.setup()
        self.get_cookie()
        self.msg = QMessageBox()
        self.center()        
    def setup(self):
        self.box = QVBoxLayout(self)
        self.web = MyWebEngineView()
        self.web.resize(1280, 720)
        self.web.load(QUrl("https://banhang.shopee.vn/"))
        self.web.loadFinished.connect(self.on_load_finished)
        self.box.addWidget(self.web)
        self.web.show()


    def on_load_finished(self):
        if status == 0:
            self.web.page().runJavaScript("document.getElementsByClassName('account-name').length", self.check)
            self.on_load = QTimer.singleShot(1000,self.on_load_finished)

    def check(self,i):
        if i == 1:
            self.web.page().runJavaScript("document.getElementsByClassName('account-name')[0].innerHTML", self.callback_function)        

    def callback_function(self,html):
        global status
        if html != None:
            status = 1 

    def get_cookie(self):      
        if status == 1:        
            cookie = self.web.get_cookie()
            shopee_info_json = Network.get_info_account_shopee(self,cookie)
            with open("temp//data.json") as json_file:  #Get username_az
                data = json.load(json_file)



            # Check for duplicates shopee id_sp on mongodb, if not, create a new shop with blank info.
            if not Database_mongoDB.check_shopee_username(self,data['username_az'],shopee_info_json['shopid']):
                Database_mongoDB.insert_new_shopee_mongodb(self,data['username_az'],cookie,shopee_info_json['id'],shopee_info_json['shopid'],shopee_info_json['username'])
                self.show_popup('Thành Công','Thành Công',f'Bạn đã thêm thành công tài khoản {shopee_info_json["username"]}.',True)
            else:

                for x in range(len(data['shopee'])):
                    if data['shopee'][x]['shop_name'] == shopee_info_json["username"]:
                        shop_c = x

                Database_mongoDB.extend_cookie(self,data['id_wp'],shop_c,cookie)
                self.show_popup('Cảnh Báo','Gia Hạn Thành Công',f'Tài khoản {shopee_info_json["username"]} đã có.\nĐã GIA HẠN thành công',False)
            self.close()
        elif status == 0:      
            time = QTimer.singleShot(1000,self.get_cookie)
        elif status == 2:      
            self.close()

    def show_popup(self,title,info,notification,c=True):      
        self.msg.setWindowTitle(title)
        self.msg.setText(notification)
        self.msg.setInformativeText(info)
        if c == True:
            self.msg.setIconPixmap(QPixmap("img//success.png"))
        else:
            self.msg.setIconPixmap(QPixmap("img//warning.png"))
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.exec_()
    def closeEvent(self,event):
        global status
        status = 2

    def center(self):
        frameGm = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        
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
