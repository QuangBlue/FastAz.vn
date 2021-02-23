import pymongo, json
import backend.users


# client = pymongo.MongoClient("mongodb+srv://quang_db:Thangkhung123@cluster0.cv2te.mongodb.net/shopee_db?retryWrites=true&w=majority")
# db = client['Shopee_Master_Tool_Database'] Create a database, if it already exists, skips
# Collection == table
# Create Shopee__Registered_Users Collection
# ShopeeRegisteredUsers = db['Shopee__Registered_Users']
# Get database and collection
# db = client.get_database("shopee_db")
# registered_Users_Collection = db.get_collection("user_db")

class Database_mongoDB:
    def __init__(self):
        # Instantianiate all static variables for the purpose of using shared database instances accross multiple files.
        Database_mongoDB.client = None
        Database_mongoDB.db = None
        Database_mongoDB.registered_Users_Collection = None

    def connect_to_mongoDB(self):
        Database_mongoDB.client = pymongo.MongoClient(
        "mongodb+srv://huy8208:741456963@shopeemastertoolcluster.n4haz.mongodb.net/Shopee_Master_Tool_Database?retryWrites=true&w=majority")
        try:
            Database_mongoDB.db = Database_mongoDB.client.get_database("Shopee_Master_Tool_Database")
            Database_mongoDB.registered_Users_Collection = Database_mongoDB.db.get_collection("Shopee__Registered_Users")
        except pymongo.errors.ConnectionFailure as error:
            print(str(error))
            exit()
        finally:
            print("Connecting to database sucessfully !!!")

    def close_db_connection(self):
        Database_mongoDB.client.close()
        print("Sucessfully closing mongodb connection !!!")


    def find_and_updateDB(self,ids, data):
        Database_mongoDB.registered_Users_Collection.find_one_and_update(
            {"_id": ids},
            {"$set": data},
            upsert=True  # Set True se tao moi khi khong co du lieu
        )

    def update_all(self,old_data, new_data):  # Hàm này để update theo logic và áp dụng cho update hàng loạt qua hàm for. Từ old_data sẽ tìm và đổi thành giá trị new_data cho kết quả find đầu tiên.

        Database_mongoDB.registered_Users_Collection.update_one(
            old_data, {"$set":new_data}
        )

    def check_username_fastaz(self,username):
        if Database_mongoDB.registered_Users_Collection.count_documents({"username_az":username}) != 0:
            return True
        else:
            return False

    def check_shopee_username(self,username_az,id_sp):
        """Check shopee username by unique id_sp"""
        if Database_mongoDB.registered_Users_Collection.count_documents({"username_az" : str(username_az) ,"shopee.shop_id" :str(id_sp)}) != 0:
            return True
        else:
            return False

    def extend_cookie(self,_id,index,new_cookie ):
        Database_mongoDB.registered_Users_Collection.update(
            { "_id": _id },
            { "$set": { 
                f'shopee.{index}.cookie' : new_cookie,
                f'shopee.{index}.status_cookie' : 'True' 
            }}
            )
        with open('temp//data.json') as f:
                data = json.load(f)
        x = Database_mongoDB.registered_Users_Collection.find({'_id': _id})
        for y in x:
            data['shopee'] = y['shopee']
        with open('temp//data.json', 'w') as f:
                    json.dump(data, f)

    def add_protuct_push(self,_id,index,data):
        Database_mongoDB.registered_Users_Collection.update(
            { "_id": _id },
            { "$addToSet": { 
                f'shopee.{index}.list_push_product' :
                { '$each': data
            }}}
            )
        with open('temp//data.json') as f:
                data = json.load(f)
        x = Database_mongoDB.registered_Users_Collection.find({'_id': _id})
        for y in x:
            data['shopee'] = y['shopee']
        with open('temp//data.json', 'w') as f:
                    json.dump(data, f)

    def insert_new_shopee_mongodb(self,username_az,shop_cookies,id_sp,shop_id,shop_name):
        #SAI CANNOT CREATE NEW USER, MUST LOCATE username_az and insert new shopee to the shopee list
        Database_mongoDB.registered_Users_Collection.update(
            {"username_az": str(username_az)},
            {"$push":
                {"shopee":{"$each":[
                                { "cookie": shop_cookies,
                                    "id_sp": str(id_sp),
                                    "shop_name": str(shop_name),
                                    "shop_id": str(shop_id),
                                    "total_product": "",
                                    "total_order": "",
                                    "status_cookie": "True",
                                    "total_order": "",
                                    "reply_rating": {
                                            "rating_1star": [],
                                            "rating_2star": [],
                                            "rating_3star": [],
                                            "rating_4star": [],
                                            "rating_5star": []
                                                    },
                                    "list_push_product" : []   
                                        
                                        },
                                    ]}
                            }},
            upsert=True)

        with open('temp//data.json') as f:
                data = json.load(f)
        x = Database_mongoDB.registered_Users_Collection.find({'username_az': str(username_az)})
        for y in x:
            data['shopee'] = y['shopee']
        with open('temp//data.json', 'w') as f:
                    json.dump(data, f)

    def insert_new_user_mongodb(self,_id,username, password,token):
        newUser = backend.users.User(_id,username,password,token)
        Database_mongoDB.registered_Users_Collection.insert_one(newUser.as_dict())
