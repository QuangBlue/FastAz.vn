from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import Screen,ScreenManager
from kivy.uix.behaviors import ButtonBehavior 
from kivy.uix.image import Image  
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

Config.set('graphics', 'resizable', False) 
Window.size = (1920 ,1080)


class WelcomeScreen(Screen):
    pass

class SignInScreen(Screen):
    pass

class CreateUserScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(WelcomeScreen(name = 'welcomescreen'))
sm.add_widget(SignInScreen(name = 'signinscreen'))
sm.add_widget(CreateUserScreen(name = 'createuserscreen'))



class FastAZ(MDApp):
    def build(self):
        self.theme_cls.primary_palette = 'Cyan'
        # self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_hue = "A700"
        self.strng = Builder.load_file('welcome.kv')
        return self.strng
    
    def sign_up_screen(self):
        self.strng.current = 'createuserscreen'
        self.strng.transition.direction = 'left'

    def sign_in_screen(self):
        self.strng.current = 'signinscreen'
        self.strng.transition.direction = 'left'
    
    def create_user_database(self):
        # Các Biến Trong Input
        self.username_create = self.strng.get_screen('createuserscreen').ids.username_create.text
        self.password_create = self.strng.get_screen('createuserscreen').ids.password_create.text
        self.email_create = self.strng.get_screen('createuserscreen').ids.email_create.text
        self.name_create = self.strng.get_screen('createuserscreen').ids.name_create.text
        self.phone_create = self.strng.get_screen('createuserscreen').ids.phone_create.text
        #Tạo request tới Wordpress để tạo tài khoản rồi trả lại thông tin đã tạo tại khoản

        cancel_btn_user_dialoue = MDFlatButton (text = 'Thử lại', on_release = self.close_username_dialoue)
        self.dialog = MDDialog (title = 'Tạo tài khoản', text = f'Đã tạo Username : {self.username_create}. Password : {self.password_create}. Email : {self.email_create}', size_hint = (0.5 , 0.2), buttons = [cancel_btn_user_dialoue])
        self.dialog.open()
    def sign_in_database(self):
        # Các Biến Trong Input
        self.username_text = self.strng.get_screen('signinscreen').ids.username_text_field.text
        self.password_text = self.strng.get_screen('signinscreen').ids.password_text_field.text
        # Check Thông Tin có rỗng không
        if self.username_text == '' or self.password_text == '':
            cancel_btn_user_dialoue = MDFlatButton (text = 'Thử lại', on_release = self.close_username_dialoue)
            self.dialog = MDDialog (title = 'Lỗi thiếu thông tin', text = 'Username và Password không được để trống', size_hint = (0.5 , 0.2), buttons = [cancel_btn_user_dialoue])
            self.dialog.open()
        else:
################################################################################
# 
#     CHECK TÀI KHOẢN TRÊN DATABASE RỒI TRẢ VỀ THÔNG TIN True hoặc False
# 
################################################################################  
            self.x = self.check_user_database()
            if self.x == True:
                print ('Đã Đăng Nhập Thành Cồng') # <------ Chưa thiết kế creen cho đăng nhập thành công
                
            if self.x == False:
                cancel_btn_user_dialoue = MDFlatButton (text = 'Nhập lại', on_release = self.close_username_dialoue)
                self.dialog = MDDialog (title = 'Sai thông tin đăng nhập', text = 'Username hoặc Password không đúng', size_hint = (0.5 , 0.2), buttons = [cancel_btn_user_dialoue])
                self.dialog.open()
    # HÀM CHECK TÀI KHOẢN                
    def check_user_database(self):
        self.result = False  #Demo Trả Kết Quả
        return self.result


    def close_username_dialoue(self,obj):
        self.dialog.dismiss() 

FastAZ().run()