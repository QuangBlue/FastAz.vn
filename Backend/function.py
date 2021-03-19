from backend.MongoDB_Setup import Database_mongoDB
from backend.networks import *
from main_pyqt5 import *

class WorkerThread(QThread):
    img_complete = pyqtSignal(list)

    def __init__(self,img,index):
        super().__init__()
        self.img = img
        self.index = index
    def run(self):
        for row , data_img in enumerate(self.img):
            url = f'https://cf.shopee.vn/file/{data_img}_tn'
            try:
                img = requests.get(url, timeout = 3).content
                l = [row,img,self.index]
                self.img_complete.emit(l)
            except:
                with open("img//no-image.png", "rb") as image:
                    f = image.read()
                    b = bytearray(f)
                l = [row,b,self.index]
                self.img_complete.emit(l)
         
class ThreadGetInfo(QThread):
    
    def __init__(self):
        super().__init__()

    def run(self):
        with open('temp//data.json') as f:
            d = json.load(f)
            k = d['shopee']
            if len(k) != 0:
                for i in range(len(k)):
                    cookie = k[i]['cookie']
                    r = backend.networks.Network.list_products_shopee(self,cookie,1)
                    if r['message'] == "success":
                        d['shopee'][i]['status_cookie'] = "True"
                        d['shopee'][i]['total_product'] = str(r['data']['page_info']['total'])
                        with open('temp//data.json', 'w') as f:
                            json.dump(d,f)
                        Database_mongoDB.find_and_updateDB(self,d['id_wp'],{f"shopee.{i}.status_cookie" : "True",f"shopee.{i}.total_product" : d['shopee'][i]['total_product']})
                    else:
                        d['shopee'][i]['status_cookie'] = "False"
                        with open('temp//data.json', 'w') as f:
                            json.dump(d,f)
                        Database_mongoDB.find_and_updateDB(self,d['id_wp'],{f"shopee.{i}.status_cookie" : "False"})

class ThreadGetListProduct(QThread):
    r_json = pyqtSignal(list)
    def __init__(self, cookie, page_number,keyword=""):
        super().__init__()
        self.c = cookie
        self.p = page_number
        self.k = keyword
    def run(self):
        r = backend.networks.Network.list_products_shopee(self,self.c,self.p,self.k)
        l = [r,self.p]
        self.r_json.emit(l)

class ThreadReplyReviews(QThread):
    update_k = pyqtSignal(str)

    def __init__(self,accShopee):
        super().__init__()
        self.accShopee = accShopee

    def run(self):
        while True:
            r = backend.networks.Network.getReplyReviews(self,self.accShopee['cookie'])
            if r['message'] == "success":
                if r['data']['page_info']['total'] != 0:
                    for x in r['data']['list']:
                        comment_id = x['comment_id']
                        order_id = x['order_id']
                        user_name = x['user_name']
                        rating_star = x['rating_star']
                        product_name = x['product_name']

                        for index, (rating, value_star) in enumerate(self.accShopee['reply_rating'].items()):
                            if rating_star == index + 1 :
                                if len(value_star) != 0 :
                                    ans = random.choice(value_star)  
                                    ans.replace("[NAME_PRODUCT]",product_name)
                                    ans.replace("[STAR]", str(rating_star))
                                    ans.replace("[NAME_SHOP]",self.accShopee['shop_name'])
                                    ans.replace("[NAME_CUSTOMER]",user_name)

                                    k = backend.networks.Network.realyReviews(self,self.accShopee['cookie'],order_id,comment_id,ans)
                                    self.update_k.emit(k['message'])
                                elif len(value_star) == 0:
                                    k = 'notReply'
                                    self.update_k.emit(k)
                        # time.sleep(60)

                elif r['data']['page_info']['total'] == 0:
                    k = 'done'
                    self.update_k.emit(k)
                    break
            else:
                k = 'error'
                self.update_k.emit(k)
                break

class ThreadPushProducts(QThread):

    donePushProduct = pyqtSignal(int)
    pushProductText = pyqtSignal(str)

    def __init__(self,accShopee,index):
        super().__init__()
        self.cookie = accShopee['cookie']
        self.listPush = accShopee['list_push_product']
        self.shopChoose = index
        with open('temp//data.json') as f:
            self.data = json.load(f)


    def run(self):
        for index_x , x in enumerate(self.listPush):
            if x['done'] == "False":
                ids = x['ids']
                name = x['name']
                r = backend.networks.Network.pushProduct(self,self.cookie,ids)
                try:
                    if r['code'] == 0: 
                        pushProductStr = f'Đã đẩy thành công sản phẩm - {name}'
                        self.pushProductText.emit(pushProductStr)
                        self.data['shopee'][self.shopChoose]['list_push_product'][index_x]['done'] = "True"
                        Database_mongoDB.find_and_updateDB(self,self.data['id_wp'],{f"shopee.{self.shopChoose}.list_push_product.{index_x}.done" : "True"})
                    elif r['code'] == 100010216: 
                        pushProductStr = f'Sản phẩm {name} đã được đẩy'
                        self.pushProductText.emit(pushProductStr)
                        self.data['shopee'][self.shopChoose]['list_push_product'][index_x]['done'] = "True"                       
                        Database_mongoDB.find_and_updateDB(self,self.data['id_wp'],{f"shopee.{self.shopChoose}.list_push_product.{index_x}.done" : "True"})
                    elif r['code'] == 100010217: 
                        pushProductStr = f"Đã hết lượt đẩy cho shop {self.data['shopee'][self.shopChoose]['shop_name']}."
                        self.pushProductText.emit(pushProductStr)
                        break                  
                except:
                    print(r)
            # time.sleep(60)
        d = self.data
        with open('temp//data.json', 'w') as f:
            json.dump(d,f)

        
        k = self.shopChoose
        self.donePushProduct.emit(k)