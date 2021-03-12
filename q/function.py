import requests, json, math, hashlib, random, pickle, time, os.path

def temp(idsp):
    print ('Chưa tạo Def')

# ENCODE MẬT KHẨU THEO SHOPEE
def encrypt_SHA256(password):
    sha_signature = \
        hashlib.sha256((hashlib.md5(password.encode()).hexdigest()).encode()).hexdigest()
    return sha_signature
################################################################

# TẠO CHUỖI SPC_CDS NGẪU NHIÊN
def csrftoken(length=32):
    character='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join((random.choice(character) for i in range(8))) + '-' + ''.join((random.choice(character) for i in range(4))) + '-' + ''.join((random.choice(character) for i in range(4))) + '-' + ''.join((random.choice(character) for i in range(4))) + '-' + ''.join((random.choice(character) for i in range(12)))
################################################################

# SAVE COOKIES THÀNH FILE TEXT
def save_cookies(requests_cookiejar, filename):
    with open(filename, 'wb') as f:
        pickle.dump(requests_cookiejar, f)
################################################################

# LOAD COOKIES ĐÃ LƯU
def load_cookies(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
################################################################

# ĐĂNG NHẬP SHOPEE VÀ LƯU COOKIES
def sign_in_shopee(idsp):
    q = csrftoken()
    id_sp = idsp
    pass_sh = encrypt_SHA256(tk_sp[idsp])
    session = requests.Session()
    payload = {
                'phone'        : id_sp,
                'password_hash': pass_sh,
                'remember': 'false',
            }
    url='https://banhang.shopee.vn/api/v2/login/?SPC_CDS=' + q + '&SPC_CDS_VER=2'
    response = session.request("POST",url, data = payload)
    if response.status_code != 200 :
        print (f'Đăng nhập thất bại tài khoản {idsp}. Lỗi ' + str(response.status_code))
        exit()
    save_cookies(response.cookies, f'shoppe{idsp}.txt')
    print (f'Đăng nhập thành công và đã lưu cookie cho tài khoản {idsp}.')
#################################################################

# TEST COOKIES CÒN HIỆU LỰC HAY KHÔNG
def test_sign_in_shopee(idsp):
    try:
        test = requests.get('https://banhang.shopee.vn', cookies=load_cookies(f'shoppe{idsp}.txt'))
        if test.status_code == 200:
            print (f'Đăng nhập tài khoản {idsp} còn hiệu lực.')
        else:
            print ('Đăng nhập hết hạn hoặc có lỗi. Đang thử đăng nhập lại..')
            sign_in_shopee(idsp)
    except FileNotFoundError:
        print ('Bạn chưa đăng nhập lần nào. Tiến hành đăng nhập lần đầu ...')
        sign_in_shopee(idsp)
################################################################

# TẠO DANH SÁCH ĐẨY SẢN PHẨM
def create_list_boot_products_shopee(idsp):
    q = csrftoken()
    url_ds_sp_shoppe = 'https://banhang.shopee.vn/api/v3/product/page_product_list/?SPC_CDS='+ q + f'&SPC_CDS_VER=2&page_number=1&page_size=100&list_type=live&search_type=name&source=seller_center&version=3.2.0'
    print (f'Tiến hành lấy danh sách sản phẩm của tài khoản {idsp}')
    list_sp = requests.get(url_ds_sp_shoppe, cookies=load_cookies(f'shoppe{idsp}.txt'))
    list_sp_json = json.loads(list_sp.text)
    for x in range(list_sp_json['data']["page_info"]['total']):
        print (f'Số {x+1} : ', list_sp_json['data']['list'][x]['name'] )
        x += 1
    while True:
        try:
            list_sp_day = []
            lst = set(map(int,input("\nNhập số các sản phẩm cần đẩy : ").strip().split()))
            print ('Các sản phẩm bạn muốn đẩy là :', lst )
            for i in lst:
                print (list_sp_json['data']['list'][i-1]['id'],' - ', list_sp_json['data']['list'][i-1]['name'] )
                list_sp_day.append(list_sp_json['data']['list'][i-1]['id'])
            break
        except  :
            print ('Vui lòng nhập đúng cú pháp. Số sản phẩm và cách nhau bởi khoảng trắng. Vui lòng nhập lại')
    with open(f'list_sp_day{idsp}.txt', 'wb') as f:
        pickle.dump(list_sp_day, f)
################################################################

# SAVE DANH SÁCH
def save_sp_day(list_shopee, filename):
    with open(filename, 'wb') as f:
        pickle.dump(list_shopee, f)
################################################################

# LOAD DANH SÁCH
def load_sp_day(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)
################################################################

# ĐẨY SẢN PHẨM SHOPEE THEO LIST ĐÃ ĐƯỢC TẠO TRƯỚC ĐÓ
def boot_products_shopee(idsp):
    try:
        q = csrftoken()
        u = load_cookies(f'shoppe{idsp}.txt')
        g = requests.cookies.RequestsCookieJar()
        g.set(domain='.shopee.vn',name='SPC_CDS',value=f"{q}")
        u.update(g)
        url = f'https://banhang.shopee.vn/api/v3/product/boost_product/?version=3.1.0&SPC_CDS={q}&SPC_CDS_VER=2'
        payload = load_sp_day(f'list_sp_day{idsp}.txt')
        if len(payload) > 5:
            k =5
        else:
            k = len(payload)
        b = random.sample(payload, k = k )
        print (b)
        try:
            for x in range(len(b)):
                r = requests.post(url,cookies=u,json={'id' : b[x]})
                k = json.loads(r.text)
                if k['code'] == 0: 
                    print (f'Đã đẩy thành công sản phẩm {b[x]} ')
                if k['code'] == 100010216: 
                    print (f'Sản phẩm {b[x]} đã được đẩy')
                if k['code'] == 100010217: 
                    print (f'Đã hết lượt đẩy.')
                    break
            print ('Kết thúc việc đẩy và đợi 4 tiếng sau')
        except:
            print('Đã có lỗi')
    except FileNotFoundError:
        print ('Bạn chưa tạo danh sách đẩy. Tiến hành tạo danh sách ...')
        create_list_boot_products_shopee(idsp)

################################################################

# TRẢ LỜI ĐÁNH GIÁ
def reply_reviews(idsp):
    url_list_rate = 'https://banhang.shopee.vn/api/v3/settings/search_shop_rating_comments/'
    so_trang = 1
    stt_danhgia = 1
    try :       
        while True:         
            list_rate = requests.get(url_list_rate, cookies=load_cookies(f'shoppe{idsp}.txt'))
            list_rate_json = json.loads(list_rate.text)
            i = 0
            so_danh_gia = list_rate_json['data']['page_info']['total']
            if so_danh_gia == 0 :
                break
            print (f'Còn tổng cộng {so_danh_gia} đánh giá cần trả lời. Tiếp tục đánh giá ...')
            while i < so_danh_gia and i < 20 :
                for x in range(5) :
                    if list_rate_json['data']['list'][i]['rating_star'] == x+1 :
                        reply_rate = {"order_id" : list_rate_json['data']['list'][i]['order_id'],"comment_id" : list_rate_json['data']['list'][i]['comment_id'], "comment" : ask_rate[x+1] }
                        url_reply_rate = 'https://banhang.shopee.vn/api/v3/settings/reply_shop_rating/'
                        post_reply_rate = requests.post(url_reply_rate, json = reply_rate, cookies=load_cookies(f'shoppe{idsp}.txt'))
                i += 1
                print (f'Đã trả lời {stt_danhgia} đánh giá.')
                stt_danhgia += 1
            else :
                print (f'Đã trả lời xong trang số {so_trang}.')
                so_trang += 1
                time.sleep(3)               
        print (f'Đã trả lời xong toàn bộ tài khoản {idsp}.')   
    except :      
        print ('Không thể trả lời đánh giá vì có lỗi.')
        exit()
################################################################

# HÀNH ĐỘNG TRẢ LỜI ĐÁNH GIÁ SAU KHI LỰA CHỌN TÀI KHOẢN THỰC THI
def action_reply_reviews(choose = 0):
    if int(choose) == 0 :
        for y in range(len(tk_sp)):
            reply_reviews(list(tk_sp.keys())[y])
    if int(choose) != 0 :
        reply_reviews(list(tk_sp.keys())[int(choose)-1])
################################################################

# HÀNH ĐỘNG ĐẨY SẢN PHẨM SAU KHI LỰA CHỌN TÀI KHOẢN THỰC THI
def action_boot_products(choose = 0):
    if int(choose) == 0 :
        for y in range(len(tk_sp)):
            if os.path.isfile(f'list_sp_day{list(tk_sp.keys())[y]}.txt'):
                pass
            else :
                print ("Bạn chưa tạo danh sách đẩy sản phẩm. Tiến hành tạo danh sách sản phẩm đẩy")
                create_list_boot_products_shopee(list(tk_sp.keys())[y])
                print ('Đã tạo danh sách dẩy. Tiến hành đẩy sản phẩm')
            boot_products_shopee(list(tk_sp.keys())[y])
    if int(choose) != 0 :
        if os.path.isfile(f'list_sp_day{list(tk_sp.keys())[int(choose)-1]}.txt'):
            pass
        else :
            print ("Bạn chưa tạo danh sách đẩy sản phẩm. Tiến hành tạo danh sách sản phẩm đẩy")
            create_list_boot_products_shopee(list(tk_sp.keys())[int(choose)-1])
            print ('Đã tạo danh sách dẩy. Tiến hành đẩy sản phẩm')
        boot_products_shopee(list(tk_sp.keys())[int(choose)-1])
