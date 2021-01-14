from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.config import Config
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.network.urlrequest import UrlRequest
import urllib.parse  # Encoder for UrlRequest
import certifi  # Certificate for UrlRequest
import json

Config.set('graphics', 'resizable', False)
Window.size = (1920, 1080)
# TẠO SCREEN CẦN 3 BƯỚC
# BƯỚC 1 TẠO CLASS CHO SCREEN
class WelcomeScreen(Screen):
    pass

class SignInScreen(Screen):
    pass

class CreateUserScreen(Screen):
    pass

class DashBoardScreen(Screen):
    pass

class Screen_1(Screen):
    pass

class Screen_2(Screen):
    pass

class Screen_3(Screen):
    pass

class Screen_4(Screen):
    pass

# BƯỚC 2 ADD CLASS CHO SCREEN VÀO SCREEN MANAGER
# BƯỚC 3 ADD VÀO FILE KV
sm = ScreenManager()
sm.add_widget(WelcomeScreen(name = 'welcomescreen'))
sm.add_widget(SignInScreen(name = 'signinscreen'))
sm.add_widget(CreateUserScreen(name = 'createuserscreen'))
sm.add_widget(DashBoardScreen(name = 'dashboardscreen'))



class FastAZ(MDApp):
    def __init__(self, **kwargs):
        """ Declares all variables in here """
        super().__init__(**kwargs)
        self.LOGIN_URL = 'http://fastaz.vn/wp-json/jwt-auth/v1/token'
        self.CREATE_ACCOUNT_URL = 'http://fastaz.vn/'
        self.login_state = False

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
        username = self.strng.get_screen('createuserscreen').ids.username_create.text
        password = self.strng.get_screen('createuserscreen').ids.password_create.text
        email = self.strng.get_screen('createuserscreen').ids.email_create.text
        name = self.strng.get_screen('createuserscreen').ids.name_create.text
        phone = self.strng.get_screen('createuserscreen').ids.phone_create.text

        params = urllib.parse.urlencode({'user_name': username,
                                         'password': password,
                                         'first_name': name,
                                         'phone': phone,
                                         'email': email,
                                         'swpm_api_action': 'create',
                                         'key': 'e3003c44deff96ebe7db442100f3b473'})
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}

        UrlRequest(self.CREATE_ACCOUNT_URL, req_body=params,
                   on_success=self.create_account_validation,
                   req_headers=headers,
                   on_error=self.sign_in_error, ca_file=certifi.where())

        # Tạo request tới Wordpress để tạo tài khoản rồi trả lại thông tin đã tạo tại khoản
        # unsuccessful_sign_up_dialog = self.create_dialog('Tạo tài khoản'
        #                                                  ,
        #                                                  f'Đã tạo Username : {username}. Password : {password}. Email : {email}'
        #                                                  , 'Thử lại', lambda a: unsuccessful_sign_up_dialog.dismiss())
        # unsuccessful_sign_up_dialog.open()



    def sign_in_database(self):
        # Các Biến Trong Input
        username_text = self.strng.get_screen('signinscreen').ids.username_text_field.text
        password_text = self.strng.get_screen('signinscreen').ids.password_text_field.text

        if username_text == '' or password_text == '':
            missing_info_dialog = self.create_dialog(dialog_title='Lỗi thiếu thông tin',
                                                     dialog_text='Username và Password không được để trống',
                                                     button_text='Thử lại'
                                                     , button_on_release=lambda a: missing_info_dialog.dismiss())
            missing_info_dialog.open()

        print("Attempting to sign user in: ", username_text, password_text)
        params = urllib.parse.urlencode({'username': username_text, 'password': password_text})
        headers = {'Content-type': 'application/x-www-form-urlencoded',
                   'Accept': 'text/plain'}
        UrlRequest(self.LOGIN_URL, req_body=params,
                   on_success=self.sign_in_validation,
                   req_headers=headers,
                   on_error=self.sign_in_error, ca_file=certifi.where())

    def sign_in_validation(self, urlrequest, log_in_data):
        sign_in_code_status = log_in_data['success']  # Boolean value
        if sign_in_code_status:
            print('Đã Đăng Nhập Thành Công')  # <------ Chưa thiết kế creen cho đăng nhập thành công
            print(log_in_data)
            self.strng.current = 'dashboardscreen'
            self.strng.transition.direction = 'left'             
            # membershipLevel = int(log_in_data['member_data']['membership_level'])
            # if membershipLevel == 2:
            #     print('Đây là tài khoản Free')
            # elif membershipLevel == 3:
            #     print('Đây là tài khoản Vip')
        else:
            print('Đăng nhập không thành công')
            unsuccessful_login_dialog = self.create_dialog('Sai thông tin đăng nhập',
                                                           'Username hoặc Password không đúng', 'Nhập lại',
                                                           lambda a: unsuccessful_login_dialog.dismiss())
            unsuccessful_login_dialog.open()

    def sign_in_error(self, *args):
        # Required by Urlrequest
        print("Sign in error", args)

    def create_dialog(self, dialog_title: str, dialog_text: str, button_text: str, button_on_release) -> MDDialog:
        """ Create a pop-up dialog with custom input parameters"""
        dialog = MDDialog(title=dialog_title,
                          text=dialog_text,
                          size_hint=(0.5, 0.2), buttons=[MDFlatButton(text=button_text, on_release=button_on_release)])
        return dialog

    def clear_user_sign_up_fields(self):
        # Clear text fields
        self.strng.get_screen('createuserscreen').ids.username_create.text = ''
        self.strng.get_screen('createuserscreen').ids.password_create.text = ''
        self.strng.get_screen('createuserscreen').ids.email_create.text = ''
        self.strng.get_screen('createuserscreen').ids.name_create.text = ''
        self.strng.get_screen('createuserscreen').ids.phone_create.text = ''
    

    def create_account_validation(self,urlrequest, sign_up_data):
        sign_up_result = json.loads(sign_up_data)
        print(sign_up_result)
        if sign_up_result['result'] == 'success':
            print("Create account successfully")
            self.clear_user_sign_up_fields()
            self.strng.current = 'signinscreen'
        elif sign_up_result['result'] == 'failure' and 'email' in sign_up_result['errors']:  # Both username and email already
            # existed error!
            print("Fail to create account")
            sign_up_failure_dialog = self.create_dialog('Tạo account không thành không'
                                                        ,"Username ho email đã được đăng ký. Bạn hãy thử đăng ký lại "
                                                         "nhé. "
                                                        ,'Thử Lại '
                                                        ,lambda a:sign_up_failure_dialog.dismiss())
            sign_up_failure_dialog.open()
        elif sign_up_result['result'] == 'failure':
            print("Fail to create account")
            sign_up_failure_dialog = self.create_dialog('Tạo account không thành không'
                                                        ,"Email đã được đăng ký, bạn hãy thử đăng nhập nhé.","Thử Lại"
                                                        ,lambda a:sign_up_failure_dialog.dismiss())
            sign_up_failure_dialog.open()
        else:
            print("Unidentified Sgn Up Error !!!")
    def retrieve_user_config(self):
        # check if user already had setting, if so, pull config from mongoDB
        # Else create user setting
        pass

    def update_user_config(self):
        # Update user config everytime user quits or manually update setting in dashboard.
        pass
    
    # Create Effec Button DashBoard Screen
    def button_change_color(self,x):
        l = ['bt_dashboard' , 'bt_boot_items' , 'bt_reply_ratings' , 'bt_setting']
        for k in l:
            if x == k :
                r = exec(f"self.strng.get_screen('dashboardscreen').ids.{x}.md_bg_color = (255/255, 255/255, 255/255, 1)")
                r = exec(f"self.strng.get_screen('dashboardscreen').ids.{x}.text_color = (10/255, 10/255, 10/255, 1)")
                r = exec(f"self.strng.get_screen('dashboardscreen').ids.{x}.icon_color = (10/255, 10/255, 10/255, 1)")
                for i in l:
                    if i == x:
                        continue
                    else:
                        exec(f"self.strng.get_screen('dashboardscreen').ids.{i}.text_color = (255/255, 255/255, 255/255, 1)")
                        exec(f"self.strng.get_screen('dashboardscreen').ids.{i}.icon_color = (255/255, 255/255, 255/255, 1)")
                        exec(f"self.strng.get_screen('dashboardscreen').ids.{i}.md_bg_color = (40/255, 40/255, 40/255, 1)")
                break

#THIS IS COMMENT OF QUANGBLUE

FastAZ().run()
