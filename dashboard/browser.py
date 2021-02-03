import sys
from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from backend.MongoDB_Setup import Database_mongoDB
import pickle


class Browser(QMainWindow):
    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.resize(1280, 720)
        self.webview = QWebEngineView()
        self.webview.page().profile().cookieStore().deleteAllCookies()
        self.webview.load(QUrl("https://shopee.vn/"))
        self.setCentralWidget(self.webview)
        self.webview.page().loadFinished.connect(self.__getCookieRunJs)

    def __getCookieRunJs(self):
        runJs = '''
        function getCookie(){return document.cookie}
        getCookie();
        '''
        self.webview.page().runJavaScript(runJs, self.__getCookieByJs)

    def __getCookieByJs(self, result):
        print (result)
        print ('Bắt đầu lưu')
        self.save_cookies(result,'cookie.txt')
        print ('Đã đầu lưu')

    def save_cookies(self,requests_cookiejar, filename):
        with open(filename, 'wb') as f:
            pickle.dump(requests_cookiejar, f)

    def closeEvent(self, event):
        Database_mongoDB.find_and_updateDB(self,10,{"avatar":"chuoi $10"})

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Browser()
    w.show()
    app.exec_()
