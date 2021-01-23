import sys
import PyQt5
import PyQt5.QtCore as QtCore
import PyQt5.QtGui as QtGui
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow as QMainWindow
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QRadioButton, QHBoxLayout, QDialog, QDesktopWidget
import qrc.file_img_rc
import webbrowser
import time

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


    def check_login(self):
        textUsername = ''
        textPassword = ''

        def showMessage(message):
            self.frame_error.show()
            self.text_error.setText(message)

        # CHECK USER
        if not self.username.text():
            textUsername = 'Username đang trống '
        else:
            textUsername = ''

        # CHECK PASSWORD
        if not self.password.text():
            textPassword = 'Password đang trống '
        else:
            textPassword = ''

        # CHECK FIELDS
        if textUsername + textPassword != '':
            text = textUsername + textPassword
            showMessage(text)
        else:
            text = "Đăng nhập thành công"
            if self.checkBox_savepass.isChecked():
                text= text + " | Đã lưu mật khẩu"
            showMessage(text)
            dashboard_screen = DashboardScreen()
            widget.addWidget(dashboard_screen)
            widget.setCurrentIndex(widget.currentIndex()+1)

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
        textUsername_create = ''
        textPassword_create = ''
        textEmail_create = ''

        def showMessage(message):
            self.frame_error.show()
            self.text_error.setText(message)

        # CHECK USER
        if not self.username_create.text():
            textUsername_create = 'Username đang trống '
        else:
            textUsername_create = ''

        # CHECK PASSWORD
        if not self.pass_create.text():
            textPassword_create = 'Password đang trống '
        else:
            textPassword_create = ''
        
        # CHECK EMAIL
        if not self.email_create.text():
            textEmail_create = 'Email đang trống '
        else:
            textEmail_create = ''

        # CHECK FIELDS
        if textUsername_create + textPassword_create + textEmail_create != '':
            text = textUsername_create + textPassword_create + textEmail_create
            showMessage(text)
        else:
            text = "Đăng ký thành công"
            showMessage(text)


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
        self.bt_dangky.clicked.connect(self.sign_up_screen)
        self.bt_reset_password.clicked.connect(self.send_code_reset)

    def send_code_reset(self):

        def showMessage(message):
            self.frame_error.show()
            self.text_error.setText(message)

        if not self.email_reset.text():
            text = 'Vui lòng nhập Email đăng ký'
            showMessage(text)
        else:
            result = True
            if result == False: ##################### <------ Làm hàm điều kiện
                text = 'Email không chính xác hoặc chưa đăng ký'
                showMessage(text)
            elif result == True:
                set_new_password_screen = SetNewPasswordScreen()
                widget.addWidget(set_new_password_screen)
                widget.setCurrentIndex(widget.currentIndex()+1)
            

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
        self.bt_set_new_password.clicked.connect(self.check_code)

    def check_code(self):
        if not self.email_set.text() or not self.password_set.text() or not self.password_set_1.text() or not self.code_set.text():
            self.text_error.setText('Vui lòng nhập đủ thông tin')
        elif self.password_set.text() != self.password_set_1.text():
            self.text_error.setText('Mật khẩu xác nhận không chính xác')
        else:
            result = True##################### <------ Làm hàm điều kiện
            if result == False:
                self.text_error.setText('Email hoặc CODE không đúng')
            elif result == True:
                self.text_error.setText('Đã đặt lại mật khẩu thành công chuyển tới Đăng Nhập sau 3s')

                # sign_in_screen = SignInScreen()
                # widget.addWidget(sign_in_screen)
                # widget.setCurrentIndex(widget.currentIndex()+1) 
            
    def back_to_welcome(self):
        welcome_screen = WelcomeScreen()
        widget.addWidget(welcome_screen)
        widget.setCurrentIndex(widget.currentIndex()+1)

GLOBAL_STATE = 0

class DashboardScreen(QMainWindow):
    def __init__(self):
        super(DashboardScreen,self).__init__()
        loadUi("ui//dashboard.ui",self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        
        self.btn_minimize.clicked.connect(lambda: self.showMinimized())
        self.btn_maximize_restore.clicked.connect(lambda: self.restore_or_maximize())
        self.btn_close.clicked.connect(lambda: self.close())

    def restore_or_maximize(self):
        pass

    
    def showMinimized(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    welcome_screen = WelcomeScreen()
    widget.addWidget(welcome_screen)
    # widget.setFixedWidth(1920)
    # widget.setFixedHeight(1080)
    widget.show()
    app.exec_() 