import requests
import main_pyqt5
import backend.loading

class Network:

    @backend.loading.setWaitCursor
    def sign_in(self,username,password):
        try:
            data = {
                'username' : username,
                'password' : password
            }
            x = requests.post('http://fastaz.vn/wp-json/jwt-auth/v1/token', data=data)
        except (requests.exceptions.HTTPError,requests.exceptions.ConnectionError,requests.exceptions.Timeout,requests.exceptions.RequestException) as err:
            print(str(err))
            main_pyqt5.ResetPasswordScreen.show_popup(self)
            raise Exception("Lỗi Server!!!")
        else:
            return x.json()

    @backend.loading.setWaitCursor
    def sign_in_token(self,token):
        try:
            headers = {
                'Authorization' : 'Bearer '+ token
            }
            x = requests.post('http://fastaz.vn/wp-json/jwt-auth/v1/token/validate', headers=headers)
        except (requests.exceptions.HTTPError,requests.exceptions.ConnectionError,requests.exceptions.Timeout,requests.exceptions.RequestException) as err:
            print(str(err))
            main_pyqt5.ResetPasswordScreen.show_popup(self)
            raise Exception("Lỗi Server!!!")
        else:
            return x.json()

    @backend.loading.setWaitCursor
    def sign_up(self,user_name,password,name,phone,email):
        try:
            data = {'user_name': user_name,
                     'password': password,
                     'first_name': name,
                     'phone': phone,
                     'email': email,
                     'swpm_api_action': 'create',
                     'key': 'e3003c44deff96ebe7db442100f3b473'}
            x = requests.post('http://fastaz.vn/', data = data)
        except (requests.exceptions.HTTPError,requests.exceptions.ConnectionError,requests.exceptions.Timeout,requests.exceptions.RequestException) as err:
            print(str(err))
            main_pyqt5.ResetPasswordScreen.show_popup(self)
            raise Exception("Lỗi Server!!!")
        else:
            return x.json()

    #Reset Password Có 2 bước cho user
    #
    # B1 : tạo yêu cầu vào hệ thống sẽ gửi 1 đoạn code 4 chữ số cho khách hàng qua email - Dùng hàm reset_password(email)
    # B2 : nhập email cũ + password mới + mật mã vừa gửi qua email - Dùng hàm set_new_password(email,password,code)

    @backend.loading.setWaitCursor
    def reset_password(self,email):
        try:
            data = {
                'email' : email
            }
            url = 'http://fastaz.vn/wp-json/bdpwr/v1/reset-password'
            r = requests.post(url, data=data)
        except (requests.exceptions.HTTPError,requests.exceptions.ConnectionError,requests.exceptions.Timeout,requests.exceptions.RequestException) as err:
            print(str(err))
            main_pyqt5.ResetPasswordScreen.show_popup(self)
            raise Exception("Lỗi Server!!!")
        else:
            return r.json()

    @backend.loading.setWaitCursor
    def set_new_password(self,email,password,code):
        try:
            data = {
                'email' : email,
                'password': password,
                'code' : code
            }
            url = 'http://fastaz.vn/wp-json/bdpwr/v1/set-password'
            r = requests.post(url, data=data)
        except (requests.exceptions.HTTPError,requests.exceptions.ConnectionError,requests.exceptions.Timeout,requests.exceptions.RequestException) as err:
            print(str(err))
            main_pyqt5.ResetPasswordScreen.show_popup(self)
            raise Exception("Lỗi Server!!!")
        else:
            return r.json()

if __name__ == '__main__':
    pass
    # reset_password('quangblue2401@gmail.com')
    # set_new_password('quangblue2401@gmail.com','Quang123456',9405)
