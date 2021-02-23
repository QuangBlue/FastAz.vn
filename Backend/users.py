"""User Class and Product Class used by front-end GUI and backend MongoDB
    Shopee Data -> User -> Show front-end GUI -> Push to MongoDB

User data structure:
{"_id": <int>,
"Username" : <string>,
"Password" : <string>,
"Avatar" : <string>,
"Token" : <string>,
"Shopee": <list>,
"List_data_push_product" : {
        Product_id:{ "Product_name" : <string>, "Product_quantity": <int>, "Product_img": <string>}
        ...
    }
}

Specification:
Username : indexed, unique
Token : indexed, unique
Product_id: indexed, unique


{'success': True, 'statusCode': 200, 'code': 'jwt_auth_valid_credential', 'message': 'Credential is valid', 'data': {'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwOlwvXC9mYXN0YXoudm4iLCJpYXQiOjE2MTE5OTU2NzIsIm5iZiI6MTYxMTk5NTY3MiwiZXhwIjoxNjEyNjAwNDcyLCJkYXRhIjp7InVzZXIiOnsiaWQiOjEwfX19.MhcityYV1yxr02_5ILfbG7GxlSB-27540MpQKR_k1Ho', 'id': 10, 'email': 'huy8208@gmail.com'
, 'nicename': 'huy_admin', 'firstName': 'huy_admin', 'lastName': '', 'displayName': 'huy_admin'}}
"""
import json


# keo du lieu tu shopee _> app
# Không cần tự add thêm field mới
# Khong can check neu 2 dua no khac nhau => lien tuc update cai key-values pair của productID đó theo thằng username n
# Chỉnh sửa lại _list_data_push_product
# Viet def update productID dựa trên username và token

# Sau này khi có nhiều khách hàng:
# Chỉ update product ID (dựa vào account nào) khi nó khác nhau giữa shopee và mongodb thì mới update.

class Shopee:
    def __init__(self,shop_cookie = "",shop_id = "",shop_name = ""):
        self.data = {"cookie":shop_cookie,
            "id_sp":shop_id,
            "shop_name":shop_name,
            "total_product":"",
            "total_order":"",
            "status_cookie":"",
            "reply_rating":{
                "rating_1star":[]
                ,"rating_2star":[]
                ,"rating_3star":[]
                ,"rating_4star":[]
                ,"rating_5star":[]},
            "list_push_product" : []               
                }
    def as_dict(self):
        return self.data

    def edit_reply_rating(self,rating_number,array):
        self.data['reply_rating'][rating_star_number] = array

    def append_to_rating_number(self,rating_number,content):
        self.data['reply_rating'][rating_number].append(content)

class Product:
    def __init__(self, productID=None, productName=None, productQuantity=None, productImage=None):
        try:
            self._product_id = str(productID)
            self._product_name = str(productName)
            self._product_quantity = int(productQuantity)
            self._product_img = str(productImage)

        except ValueError as e:
            print(e)

    def get_product_id(self):
        return self._product_id

    def get_product_name(self):
        return self._product_name

    def get_product_quantity(self):
        return self._product_quantity

    def get_product_img(self):
        return self._product_img


class User:
    def __init__(self, _id=None, username="", password="",token="", avatar="", cookies="",id_sp="",shop_name=""):
        try:
            self._id = _id #Double check
            self._username_az = str(username)
            self._password_az = str(password)
            self._avatar = str(avatar)
            self._token = token
            self._shopee = []
            # self._list_data_push_product = dict()
        except ValueError as e:
            print(e)

    def __str__(self):
        """Print out user's object as str"""
        return "Username: " + str(self._username_fastaz) + "\n" + "Password: " + self._password + \
               "\n" + "Avatar: " + self._avatar + "\n" + self._token + "\n" + self._shopee
            #    + json.dumps(self._list_data_push_product, indent=4)

    def as_dict(self):
        dict1 = {
            "_id": self._id,
            "username_az": self._username_az,
            "password_az": self._password_az,
            "token":self._token,
            "avatar": self._avatar,
            "shopee": self._shopee
            }
        # dict1.update(self._list_data_push_product)
        return dict1

    def add_new_shopee_shop(self,shop_cookies,shop_id,shop_name):
        newShop = Shopee(shop_cookies,shop_id,shop_name)
        self._shopee.append(newShop.as_dict())

    def add_new_product(self, productID, productName, productQuantity, productImage):
        """ Add sản phẩm mới vào user
            Ex:
                user1 = User(username="Huy", password="yes", avatar="img1234", token="token")
                user1.add_new_product(productID, productName, productQuantity, productImage)
        """
        self._new_product = Product(productID, productName, productQuantity, productImage)
        self._list_data_push_product["Product"] = \
            {"Product_ID": self._new_product.get_product_id(),
             "Product_name": self._new_product.get_product_name(),
             "Product_quantity": self._new_product.get_product_quantity(),
             "Product_img": self._new_product.get_product_img()}
