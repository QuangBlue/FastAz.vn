from main_pyqt5 import *
from dashboard.dashboard import *
from backend.function import *

class ProductPush:


    def setDataProductPush(self):
        self.tableWidget_product_push.setRowCount(24)
        for k in range(self.tableWidget_product_push.rowCount()):
            self.tableWidget_product_push.setRowHeight(k, 90)

        self.tableWidget_product_push.setColumnWidth(0, 50)
        self.tableWidget_product_push.setColumnWidth(1, 100)
        self.tableWidget_product_push.setColumnWidth(2, 800)
        self.tableWidget_product_push.setColumnWidth(3, 150)
        self.tableWidget_product_push.setColumnWidth(4, 150)
        self.tableWidget_product_push.setColumnWidth(5, 150)
        self.tableWidget_product_push.setColumnWidth(6, 150)
        with open('temp//data.json') as f:
            data = json.load(f)
        shop_choose = self.checkShopChoose()
        if len(data['shopee']) != 0:         
            if len(data['shopee'][shop_choose]['list_push_product']) !=0:
                self.tableWidget_product_push.setRowCount(len(data['shopee'][shop_choose]['list_push_product']) if len(data['shopee'][shop_choose]['list_push_product']) > 24 else 24)
                for k in range(self.tableWidget_product_push.rowCount()):
                    self.tableWidget_product_push.setRowHeight(k, 90)              
                s1 = data['shopee'][shop_choose]['list_push_product']
                img = []
                for row, x in enumerate(s1):
                    self.btn_del_pp = QPushButton('')
                    self.btn_del_pp.clicked.connect(lambda: ProductPush.btnDelProductPush(self))
                    self.tableWidget_product_push.setCellWidget(row,0,self.btn_del_pp)
                    self.btn_del_pp.setStyleSheet('QPushButton { image: url(img//remove.png);background: transparent;}QPushButton:hover { image: url(img//remove_red.png);}')
                    self.tableWidget_product_push.setItem(row, 2,QTableWidgetItem(x['name']))
                    self.tableWidget_product_push.setItem(row, 3,QTableWidgetItem(x['parent_sku']))
                    self.tableWidget_product_push.setItem(row, 4,QTableWidgetItem(str(x['stock'])))
                    self.tableWidget_product_push.setItem(row, 5,QTableWidgetItem(x['normal_price']))
                    self.tableWidget_product_push.setItem(row, 6,QTableWidgetItem(x['promotion_price']))
                    self.tableWidget_product_push.setItem(row, 7,QTableWidgetItem(str(x['sold'])))
                for x in s1:
                    img.append(x['image'])
                self.workerthread1 = WorkerThread(img,'product_list_user')
                self.workerthread1.start()
                self.workerthread1.img_complete.connect(self.update_img)  
        self.writeLog('Tải sản phẩm đẩy')

    def popupAddProductPush(self):
        shop_choose = self.checkShopChoose()

        from dashboard.popupProduct import Popup_Product
        self.ui = Popup_Product(shop_choose)
        self.ui.show()
        self.ui.btn_confirm.clicked.connect(lambda: ProductPush.setDataProductPush(self))
    
    def btnDelProductPush(self):
        x = QMessageBox.warning(self, 'MessageBox', "Bạn có chắc chắn muốn xóa sản phẩm này không ?", QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)        
        with open('temp//data.json') as f:
            data = json.load(f)
        
        if x == QMessageBox.Yes:
            button = self.sender()
            index = self.tableWidget_product_push.indexAt(button.pos())
            shop_choose = self.checkShopChoose()

            self.tableWidget_product_push.removeRow(index.row())

            Database_mongoDB.registered_Users_Collection.update({"_id": data['id_wp']}, {"$unset": {f"shopee.{shop_choose}.list_push_product.{index.row()}": 1}})
            Database_mongoDB.registered_Users_Collection.update({"_id": data['id_wp']}, {"$pull": {f"shopee.{shop_choose}.list_push_product": None}})
            self.writeLog('Xóa sản phẩm đẩy')

        x = Database_mongoDB.registered_Users_Collection.find({'_id': data['id_wp']})    
        for y in x:
            data['shopee'] = y['shopee']
        with open('temp//data.json', 'w') as f:
                    json.dump(data, f)

        if len(data['shopee'][shop_choose]['list_push_product']) == 0 :
            self.btnPushProductSwitch.setChecked(False)
            UIFunctions.activeFunctions(self,self.btnPushProductSwitch.isChecked(),"pushProductSwitch")

