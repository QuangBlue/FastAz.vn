import requests


def wpSignIn(userID, password):
    data = {
        'username': userID,
        'password': password
    }
    x = requests.post('http://fastaz.vn/wp-json/jwt-auth/v1/token', data=data).json()
    return x

    if x['success']:
        id_acc = x['data']['id']
        username = x['data']['displayName']
        print(f'Đã đăng nhập thành công user {username}. Id: {id_acc}')

        data_1 = {
            'swpm_api_action': 'query',
            'key': 'e3003c44deff96ebe7db442100f3b473',
            'email': x['data']['email']
        }
        y = requests.get('http://www.fastaz.vn/', params=data_1).json()

        if y['result'] == 'success':
            membershipLevel = int(y['member_data']['membership_level'])
            if membershipLevel == 2:
                print('Đây là tài khoản Free')
            elif membershipLevel == 3:
                print('Đây là tài khoản Vip')
        elif y['result'] == "failure":
            print(y['message'])

    elif not x['success']:
        print(x['message'])


def create_use(user_name, password, first_name, last_name, email):
    data = {
        'user_name': user_name,
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'swpm_api_action': 'create',
        'key': 'e3003c44deff96ebe7db442100f3b473'
    }
    x = requests.post('http://fastaz.vn/', data=data)
    print(x.text)
