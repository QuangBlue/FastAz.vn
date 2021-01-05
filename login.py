import requests

def check_user():
    idd = input('Id: ')
    pas = input('Password: ')
    data = {
        'username' : idd,
        'password' : pas
    }
    x = requests.post('http://fastaz.vn/wp-json/jwt-auth/v1/token', data=data)

    if x.json()['success'] == True:
        id_acc = x.json()['data']['id']
        username = x.json()['data']['displayName']
        print (f'Đã đăng nhập thành công user {username}. Id: {id_acc}' )
           
        data_1 = {
            'swpm_api_action' : 'query',
            'key' : 'e3003c44deff96ebe7db442100f3b473',
            'email' : x.json()['data']['email']
        }
        y = requests.get('http://www.fastaz.vn/', params=data_1)


        if y.json()['result'] == 'success':
            if int(y.json()['member_data']['membership_level']) == 2:
                print ('Đây là tài khoản Free')
            if int(y.json()['member_data']['membership_level']) == 3:
                print ('Đây là tài khoản Vip')
        elif y.json()['result'] == "failure":
            print (y.json()['message'])

    if x.json()['success'] == False:
        print (x.json()['message'])

def create_use(user_name,password,first_name,last_name,email):
    data = {
        'user_name':user_name,
        'password' :password,
        'first_name' :first_name,
        'last_name' :last_name,
        'email' : email,
        'swpm_api_action' : 'create',
        'key' : 'e3003c44deff96ebe7db442100f3b473'
    }
    x = requests.post('http://fastaz.vn/', data = data)
    print (x.text)

if __name__ == '__main__':
    
    check_user()