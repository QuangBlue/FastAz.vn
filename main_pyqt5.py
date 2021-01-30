import sys
import PyQt5
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import qrc.file_img_rc
import webbrowser
import time



## IMPORT SCREEN
from dashboard.Dashboard import Dashboard


## Database
import Backend.networks
import Backend.MongoDB_Setup as db
import Backend.loading

# MANAGER SCREEN ---- WELCOME ----
class WelcomeScreen(QMainWindow):
    def __init__(self):
        super(WelcomeScreen,self).__init__()
        loadUi("ui//welcome.ui",self)

    # SETTING BUTTON
        self.pushButton_trangchu.clicked.connect(self.open_webbrowser)
        self.pushButton_banggia.clicked.connect(self.open_webbrowser)
        self.pushButton_huongdan.clicked.connect(self.open_webbrowser)
        self.pushButton_dangnhap.clicked.connect(self.sign_in_screen)
        self.pushButton_dangky.clicked.connect(self.sign_up_screen)

    def sign_in_screen(self):
        sign_in_screen = SignInScreen()
        widget.addWidget(sign_in_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_up_screen(self):
        sign_up_screen = SignUpScreen()
        widget.addWidget(sign_up_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def open_webbrowser(self):
        webbrowser.open('http://fastaz.vn/')


# MANAGER SCREEN ---- SIGN IN ----

class SignInScreen(QMainWindow):
    def __init__(self):
        super(SignInScreen,self).__init__()
        loadUi("ui//sign_in_screen.ui",self)
    # SETTING FRAME ERROR HIDE
        self.bt_x.clicked.connect(lambda : self.frame_error.hide())
        self.frame_error.hide()


    # SETTING BUTTON
        self.bt_back.clicked.connect(self.back_to_welcome)
        self.bt_dangky.clicked.connect(self.sign_up_screen)
        self.pushButton_login.clicked.connect(self.check_login)
        self.bt_reset_password.clicked.connect(self.reset_password_screen)
        self.password.returnPressed.connect(self.check_login)

    def check_login(self):

        def showMessage(message):
            self.frame_error.show()
            self.text_error.setText(message)

        re = Backend.networks.Network.sign_in(self,self.username.text(),self.password.text())
        if re['success']:
            print (f'Đã đăng nhập thành công user {self.username.text()}. Id: {self.password.text()}' )
            # Push len database, phai check xem da co username chua
            # Check if username already in mongodb if not => create new user
            #                                       else => skip
            if db.check_username_fastaz(self.username.text()) == False:
                # username, password, avatar,token,shopee
                db.insert_new_user_mongodb(self.username.text(),self.password.text(),None,re['data']['token'])
            self.ui = Dashboard()
            widget.close()

        elif re['success'] == False:
            showMessage(re['message'])

    def back_to_welcome(self):
        welcome_screen = WelcomeScreen()
        widget.addWidget(welcome_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_up_screen(self):
        sign_up_screen = SignUpScreen()
        widget.addWidget(sign_up_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def reset_password_screen(self):
        reset_password_screen = ResetPasswordScreen()
        widget.addWidget(reset_password_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)


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
        self.bt_dangnhap.clicked.connect(self.sign_in_screen)
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
            sign_up_result = Backend.networks.Network.sign_up(self,us,pw,fn,ph,em)
            # print(sign_up_result)
            if sign_up_result['result'] == 'success':
                print("Create account successfully")
                self.sign_in_screen()    
            elif sign_up_result['result'] == 'failure' and 'email' in sign_up_result[
                'errors']:  
                print("Sign up error!. Both username and email already existed error!")
                showMessage("Username hoặc email đã được đăng ký.  Bạn hãy thử đăng ký lại nhé.")
            elif sign_up_result['result'] == 'failure': 
                print("Sign up error!. email already existed error!")
                showMessage("Username hoặc email đã được đăng ký.  Bạn hãy thử đăng ký lại nhé.")

    def back_to_welcome(self):
        welcome_screen = WelcomeScreen()
        widget.addWidget(welcome_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_in_screen(self):
        sign_in_screen = SignInScreen()
        widget.addWidget(sign_in_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

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
        self.bt_dangnhap.clicked.connect(self.sign_in_screen)
        self.bt_dangky.clicked.connect(self.show_popup) #sign_up_screen)
        self.bt_reset_password.clicked.connect(self.send_code_reset)

    def send_code_reset(self):

        def showMessage(message):
            self.frame_error.show()
            self.text_error.setText(message)


        if not self.email_reset.text():
            text = 'Vui lòng nhập Email đăng ký'
            showMessage(text)
        else:
            request_result = Backend.networks.Network.reset_password(self,self.email_reset.text())
            # print(request_result)
            showMessage(request_result["message"])
            if request_result['data']['status'] == 200:
                Backend.loading.appWait(2000) #Can phai tim ra cach toi uu hon, bo vao trong network def
                set_new_password_screen = SetNewPasswordScreen()
                widget.addWidget(set_new_password_screen)
                widget.setCurrentIndex(widget.currentIndex()+1)
                
            # if result == False: ##################### <------ Làm hàm điều kiện

    def show_popup(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Server đang bảo trì, bạn hãy thử lại sau 30' nhé!")
        msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Close)
        msg.exec_()


    def back_to_welcome(self):
        welcome_screen = WelcomeScreen()
        widget.addWidget(welcome_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_in_screen(self):
        sign_in_screen = SignInScreen()
        widget.addWidget(sign_in_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_up_screen(self):
        sign_up_screen = SignUpScreen()
        widget.addWidget(sign_up_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

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
            request_result = Backend.networks.Network.set_new_password(self,self.email_set.text(),self.password_set.text(),self.code_set.text())
            # print(request_result)            
            showMessage(request_result['message'])
            if request_result['data']['status'] == 200:
                Backend.loading.appWait(2000) # Can phai tim ra cach toi uu hon.
                self.sign_in_screen()
                

            

    def back_to_welcome(self):
        welcome_screen = WelcomeScreen()
        widget.addWidget(welcome_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def sign_in_screen(self):
        sign_in_screen = SignInScreen()
        widget.addWidget(sign_in_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    welcome_screen = WelcomeScreen()
    widget.addWidget(welcome_screen)
    widget.resize(1920, 1080)
    widget.show()
    app.exec_()
