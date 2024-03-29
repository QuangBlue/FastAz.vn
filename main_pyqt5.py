import sys, webbrowser, json, requests , random , time, math

from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor, QFont, QImage, QPixmap, QFontDatabase, QIcon, QBrush , QPaintEvent, QPen, QPainter
from PyQt5.QtCore import pyqtSlot, pyqtProperty , QSequentialAnimationGroup, QPoint, QPointF, QRectF, QSize, Qt, QUrl, QEventLoop, QPropertyAnimation, QTimer, QEvent, QEasingCurve, QByteArray, QThread, pyqtSignal,QObject, QModelIndex
from PyQt5.QtWidgets import QCheckBox, QMainWindow, QApplication, QGraphicsDropShadowEffect, QPushButton, QSizePolicy,QWidgetItem, QSizeGrip, QMessageBox, QHBoxLayout,QVBoxLayout, QLabel, QWidget, QFrame, QStackedWidget, QTableWidgetItem, QPlainTextEdit,QTableWidget,QAbstractItemView, QLayout
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkReply, QNetworkRequest, QNetworkCookie
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage

## IMPORT SCREEN
from dashboard.dashboard import *
from backend.function import *
import qrc.file_img_rc
## Database
import backend.networks
import backend.MongoDB_Setup as db
import backend.loading
from backend.MongoDB_Setup import Database_mongoDB

# MANAGER SCREEN ---- WELCOME ----
class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen,self).__init__()
        loadUi("ui//welcome.ui",self)
    # SETTING BUTTON
        self.pushButton_trangchu.clicked.connect(self.openWebbrowser)
        self.pushButton_banggia.clicked.connect(self.openWebbrowser)
        self.pushButton_huongdan.clicked.connect(self.openWebbrowser)
        self.pushButton_dangnhap.clicked.connect(self.signInScreen)
        self.pushButton_dangky.clicked.connect(self.signUpScreen)

    def signInScreen(self):
        WelcomeScreen.savepass = "False"
        try:
            with open('temp//data.json') as f:
                WelcomeScreen.data = json.load(f)
                
        except:
            signInScreen = SignInScreen()
            MainWindow.widget.addWidget(signInScreen)
            MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)

        else:
            WelcomeScreen.savepass = WelcomeScreen.data['savepass']
            if WelcomeScreen.data['savepass'] == "True":
                re = backend.networks.Network.sign_in_token(self,WelcomeScreen.data['token'])
                if re['success'] == True:
                    print('Đăng nhập tự động')
                    MainWindow.mongo_db.connect_to_mongoDB() 
                    self.ui = LoadingScreen()
                    MainWindow.widget.hide()
                else:
                    WelcomeScreen.savepass = "False"
                    signInScreen = SignInScreen()
                    MainWindow.widget.addWidget(signInScreen)
                    MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1) 
                    
            else:        
                signInScreen = SignInScreen()
                MainWindow.widget.addWidget(signInScreen)
                MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)

    def signUpScreen(self):
        signUpScreen = SignUpScreen()
        MainWindow.widget.addWidget(signUpScreen)
        MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)


    def openWebbrowser(self):
        webbrowser.open('http://fastaz.vn/')

# MANAGER SCREEN ---- SIGN IN ----

class SignInScreen(QMainWindow):
    def __init__(self):
        super(SignInScreen,self).__init__()
        loadUi("ui//sign_in_screen.ui",self)
        MainWindow.mongo_db.connect_to_mongoDB() 
    # SETTING FRAME ERROR HIDE
        self.bt_x.clicked.connect(lambda : self.frame_error.hide())
        self.frame_error.hide()


    # SETTING BUTTON
        self.bt_back.clicked.connect(self.back_to_welcome)
        self.bt_dangky.clicked.connect(self.signUpScreen)
        self.pushButton_login.clicked.connect(self.check_login)
        self.bt_reset_password.clicked.connect(self.reset_password_screen)
        self.password.returnPressed.connect(self.check_login)

        MainWindow.widget.closeEvent = self.closeEvent

    def closeEvent(self,event):
        Database_mongoDB.close_db_connection(self)

    def check_login(self):

        def showMessage(message):
            self.frame_error.show()
            self.text_error.setText(message)

        re = backend.networks.Network.sign_in(self,self.username.text(),self.password.text())
        if re['success']:
            # KHAI BÁO BIẾN CHO CLASS
            SignInScreen.id_wp = int(re['data']['id'])
            SignInScreen.username_az = self.username.text()
            SignInScreen.password_az = self.password.text()
            SignInScreen.token = re['data']['token']
            SignInScreen.email = re['data']['email']
            if self.checkBox_savepass.isChecked():
                SignInScreen.savepass = "True"
            else:
                SignInScreen.savepass = "False"

            print (f'Đã đăng nhập thành công user {self.username.text()}. Password: {self.password.text()}' )
            self.ui = LoadingScreen()
            MainWindow.widget.hide()


        elif re['success'] == False:
            showMessage(re['message'])


    def back_to_welcome(self):
        welcome_screen = WelcomeScreen()
        MainWindow.widget.addWidget(welcome_screen)
        MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)

    def signUpScreen(self):
        signUpScreen = SignUpScreen()
        MainWindow.widget.addWidget(signUpScreen)
        MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)

    def reset_password_screen(self):
        reset_password_screen = ResetPasswordScreen()
        MainWindow.widget.addWidget(reset_password_screen)
        MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)


# MANAGER SCREEN ---- SIGN UP ----

class SignUpScreen(QMainWindow):
    def __init__(self):
        super(SignUpScreen,self).__init__()
        loadUi("ui//sign_up_screen.ui",self)

    # SETTING FRAME ERROR HIDE
        self.bt_x.clicked.connect(lambda : self.frame_error.hide())
        self.frame_error.hide()

    # SETTING BUTTON

        self.bt_back.clicked.connect(self.back_to_welcome)
        self.bt_dangnhap.clicked.connect(self.signInScreen)
        self.pushButton_signup.clicked.connect(self.check_signup)

    def check_signup(self):

        def showMessage(message):
            self.frame_error.show()
            self.text_error.setText(message)
        us = self.username_create.text()
        pw = self.pass_create.text()
        em = self.email_create.text()
        fn = self.name_create.text()
        ph = self.phone_create.text()

        input_field = [us,pw,em,fn,ph]

        if not (all(input_field)):
            showMessage("Thiếu dữ liệu đăng ký! Bạn hãy thử lại nhé.")
        else:
            sign_up_result = backend.networks.Network.sign_up(self,us,pw,fn,ph,em)
            if sign_up_result['result'] == 'success':
                print("Create account successfully")
                self.signInScreen()
            elif sign_up_result['result'] == 'failure' and 'email' in sign_up_result[
                'errors']:
                print("Sign up error!. Both username and email already existed error!")
                showMessage("Username hoặc email đã được đăng ký.  Bạn hãy thử đăng ký lại nhé.")
            elif sign_up_result['result'] == 'failure':
                print("Sign up error!. email already existed error!")
                showMessage("Username hoặc email đã được đăng ký.  Bạn hãy thử đăng ký lại nhé.")

    def back_to_welcome(self):
        welcome_screen = WelcomeScreen()
        MainWindow.widget.addWidget(welcome_screen)
        MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)

    def signInScreen(self):
        signInScreen = SignInScreen()
        MainWindow.widget.addWidget(signInScreen)
        MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)

# MANAGER SCREEN ---- RESET PASSWORD ----

class ResetPasswordScreen(QMainWindow):
    def __init__(self):
        super(ResetPasswordScreen,self).__init__()
        loadUi("ui//reset_password_screen.ui",self)

    # SETTING FRAME ERROR HIDE
        self.bt_x.clicked.connect(lambda : self.frame_error.hide())
        self.frame_error.hide()

    # SETTING BUTTON
        self.bt_back.clicked.connect(self.back_to_welcome)
        self.bt_dangnhap.clicked.connect(self.signInScreen)
        self.bt_dangky.clicked.connect(self.signUpScreen) 
        self.bt_reset_password.clicked.connect(self.send_code_reset)

    def send_code_reset(self):

        def showMessage(message):
            self.frame_error.show()
            self.text_error.setText(message)


        if not self.email_reset.text():
            text = 'Vui lòng nhập Email đăng ký'
            showMessage(text)
        else:
            request_result = backend.networks.Network.reset_password(self,self.email_reset.text())
            showMessage(request_result["message"])
            if request_result['data']['status'] == 200:
                set_new_password_screen = SetNewPasswordScreen()
                MainWindow.widget.addWidget(set_new_password_screen)
                MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)


    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Server đang bảo trì, bạn hãy thử lại sau 30' nhé!")
        msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Close)
        msg.exec_()


    def back_to_welcome(self):
        welcome_screen = WelcomeScreen()
        MainWindow.widget.addWidget(welcome_screen)
        MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)

    def signInScreen(self):
        signInScreen = SignInScreen()
        MainWindow.widget.addWidget(signInScreen)
        MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)

    def signUpScreen(self):
        signUpScreen = SignUpScreen()
        MainWindow.widget.addWidget(signUpScreen)
        MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)

# MANAGER SCREEN ---- SET NEW PASSWORD ----

class SetNewPasswordScreen(QMainWindow):
    def __init__(self):
        super(SetNewPasswordScreen,self).__init__()
        loadUi("ui//set_new_password_screen.ui",self)

    # SETTING FRAME ERROR HIDE
        self.bt_x.clicked.connect(lambda : self.frame_error.hide())

    # SETTING BUTTON
        self.bt_back.clicked.connect(self.back_to_welcome)
        self.bt_set_new_password.clicked.connect(self.reset_code_validation)

    def reset_code_validation(self):

        def showMessage(message):
            self.frame_error.show()
            self.text_error.setText(message)

        if not self.email_set.text() or not self.password_set.text() or not self.password_set_1.text() or not self.code_set.text():
            self.text_error.setText('Vui lòng nhập đủ thông tin')
            self.frame_error.show()
        elif self.password_set.text() != self.password_set_1.text():
            self.text_error.setText('Mật khẩu xác nhận không chính xác')
            self.frame_error.show()
        else:
            request_result = backend.networks.Network.set_new_password(self,self.email_set.text(),self.password_set.text(),self.code_set.text())
            # print(request_result)
            showMessage(request_result['message'])
            if request_result['data']['status'] == 200:
                backend.loading.appWait(2000) # Can phai tim ra cach toi uu hon.
                self.signInScreen()



    def back_to_welcome(self):
        welcome_screen = WelcomeScreen()
        MainWindow.widget.addWidget(welcome_screen)
        MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)

    def signInScreen(self):
        signInScreen = SignInScreen()
        MainWindow.widget.addWidget(signInScreen)
        MainWindow.widget.setCurrentIndex(MainWindow.widget.currentIndex()+1)

class LoadingScreen(QMainWindow):
    def __init__(self):
        super(LoadingScreen,self).__init__()
        loadUi("ui//loading_screen.ui",self)
        self.counter = 0
        ## REMOVE TITLE BAR
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        ## DROP SHADOW EFFECT
        # self.shadow = QGraphicsDropShadowEffect(self)
        # self.shadow.setBlurRadius(20)
        # self.shadow.setXOffset(0)
        # self.shadow.setYOffset(0)
        # self.shadow.setColor(QColor(0, 0, 0, 60))
        # self.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        # CHANGE DESCRIPTION

        # Initial Text
        self.label_description.setText("<strong>CHÀO BẠN</strong> ĐẾN VỚI ỨNG DỤNG")

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## END ##

    ##  APP FUNCTIONS
    ########################################################################
    def progress(self):

        # SET VALUE TO PROGRESS BAR
        self.progressBar.setValue(self.counter)

        if self.counter == 10:
            self.label_description.setText("<strong>KIỂM TRA</strong> PHIÊN BẢN")
            if WelcomeScreen.savepass == "False":
                self.data ={}
                self.data['id_wp'] = SignInScreen.id_wp
                self.data['username_az'] = SignInScreen.username_az
                self.data['password_az'] = SignInScreen.password_az
                self.data['email'] = SignInScreen.email
                self.data['token'] = SignInScreen.token
                self.data['savepass'] = SignInScreen.savepass
                self.data['theme'] = 'dark'
                self.data['shopee'] = []

        if self.counter == 22:
            self.label_description.setText("<strong>TẢI</strong> THÔNG TIN NGƯỜI DÙNG")

        if self.counter == 24:
            
            # Checking for the first time if this is a new user, if so, insert user info to mongodb database.
            if WelcomeScreen.savepass == "False":
                print ('Đang check tài khoản')
                if Database_mongoDB.check_username_fastaz(self,SignInScreen.username_az) == False:
                    Database_mongoDB.insert_new_user_mongodb(self,SignInScreen.id_wp,SignInScreen.username_az,SignInScreen.password_az,SignInScreen.token)
                    print ('Đã thêm data lên MongoDB')
                else:
                    x = Database_mongoDB.registered_Users_Collection.find({'_id': SignInScreen.id_wp})
                    for y in x:
                        self.data['shopee'] = y['shopee']
                self.counter += 12
            if WelcomeScreen.savepass == "True":
                data_t = WelcomeScreen.data
                x = Database_mongoDB.registered_Users_Collection.find({'_id':  data_t['id_wp']})
                for y in x:
                    data_t['shopee'] = y['shopee']
                with open('temp//data.json', 'w') as f:
                    json.dump(data_t, f)

        if self.counter == 50:
            if WelcomeScreen.savepass == "False":
                with open('temp//data.json', 'w') as f:
                    json.dump(self.data, f)
            self.label_description.setText("<strong>TẢI</strong> TÀI NGUYÊN ỨNG DỤNG")
            
        if self.counter == 75:           
            self.label_description.setText("<strong>TẢI</strong> THÔNG TIN TÀI KHOẢN")
        if self.counter == 99:
            self.label_description.setText("<strong>TẢI</strong> THÔNG TIN KHUYẾN MÃI")
            
        # CLOSE SPLASH SCREE AND OPEN APP
        if self.counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            from dashboard.dashboard import Dashboard
            self.main = Dashboard()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        self.counter += 1

class MainWindow():
    def __init__(self):       
        MainWindow.widget = QStackedWidget()
        welcome_screen = WelcomeScreen()
        MainWindow.mongo_db = db.Database_mongoDB()
        MainWindow.widget.addWidget(welcome_screen)
        MainWindow.widget.resize(1280, 720)
        QFontDatabase.addApplicationFont('font/Nunito/Nunito-Regular.ttf')
        MainWindow.widget.show()       

if __name__ == '__main__': 
    app = QApplication(sys.argv)
    MainWindow()
    app.exec_()