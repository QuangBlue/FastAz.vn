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
    def __init__(self, cookie, page_number):
        super().__init__()
        self.c = cookie
        self.p = page_number
    def run(self):
        r = backend.networks.Network.list_products_shopee(self,self.c,self.p)
        l = [r,self.p]
        self.r_json.emit(l)

