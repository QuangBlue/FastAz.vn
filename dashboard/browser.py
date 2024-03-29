import sys,requests, json , shutil, os
from PyQt5.QtCore import QUrl, Qt ,QTimer
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from PyQt5.QtGui import QFont, QPixmap
from backend.MongoDB_Setup import Database_mongoDB
from backend.networks import Network

sys.setrecursionlimit(100000)

status = 0

class Browser(QWidget):
    def __init__(self, profileShopee):
        super().__init__()
        self.profileShopee = profileShopee
        self.resize(1700, 1000)
        global status
        status = 0
        self.setup()
        self.get_cookie()
        self.msg = QMessageBox()
        self.center()        
    def setup(self):
        self.box = QVBoxLayout(self)
        self.web = MyWebEngineView(self.profileShopee)
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
        pathProfile = self.web.pathProfileFunc()
        with open("temp//data.json") as json_file:  #Get username_az
            data = json.load(json_file)     
        if status == 1:        
            cookie = self.web.get_cookie()       
            shopee_info_json = Network.get_info_account_shopee(self,cookie)
            
            if not Database_mongoDB.check_shopee_username(self,data['username_az'],shopee_info_json['shopid']):
                Database_mongoDB.insert_new_shopee_mongodb(self,data['username_az'],cookie,shopee_info_json['id'],shopee_info_json['shopid'],shopee_info_json['username'],self.profileShopee)
                self.show_popup('Thành Công','Thành Công',f'Bạn đã thêm thành công tài khoản {shopee_info_json["username"]}.',True)
            else:
                for x in range(len(data['shopee'])):
                    if data['shopee'][x]['shop_name'] == shopee_info_json["username"]:
                        shop_c = x
                try:
                    path = pathProfile.replace(self.profileShopee, data['shopee'][shop_c]['pathName'])
                    shutil.rmtree(path)
                except:
                    pass
                Database_mongoDB.extend_cookie(self,data['id_wp'],shop_c,cookie,self.profileShopee)
                self.show_popup('Cảnh Báo','Gia Hạn Thành Công',f'Tài khoản {shopee_info_json["username"]} đã có.\nĐã GIA HẠN thành công',False)
            self.delFolderProfile(pathProfile)
            self.close()
        elif status == 0:      
            time = QTimer.singleShot(1000,self.get_cookie)
        elif status == 2:    
            self.close()

    def delFolderProfile(self, pathProfile):
        listName = []
        with open("temp//data.json") as json_file:  
            d = json.load(json_file)
        if len(d['shopee']) != 0:
            for x in d['shopee']:
                listName.append(x['pathName'])         
        pathNot = pathProfile.replace(pathProfile.split('/')[-1],'')
        arr = os.listdir(pathNot)
        for x in arr:
            if x not in listName and x !="Default" and x != ".DS_Store" :
                q = pathNot + x
                shutil.rmtree(q)
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
    def __init__(self,profileShopee ):
        super(MyWebEngineView, self).__init__()

        profile = QWebEngineProfile(profileShopee, self)
        webpage = QWebEnginePage(profile, self)
        self.pathProfile = profile.persistentStoragePath()
        self.setPage(webpage)

        self.page().profile().cookieStore().cookieAdded.connect(self.onCookieAdd)
        self.cookies = {}

    def onCookieAdd(self, cookie):
        name = cookie.name().data().decode('utf-8')
        value = cookie.value().data().decode('utf-8')
        self.cookies[name] = value


    def get_cookie(self):
        return self.cookies

    def pathProfileFunc(self):
        return self.pathProfile

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Browser()
    w.show()
    sys.exit(app.exec_())
