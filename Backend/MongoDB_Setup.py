import pymongo
import datetime
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

    def check_shopee_username(self,shopee_username,id_sp):
        """Check shopee username by unique id_sp"""
        if Database_mongoDB.registered_Users_Collection.count_documents({"username_az" : str(shopee_username) ,"shopee.shop_id" :str(id_sp)}) != 0:
            return True
        else:
            return False


    def insert_new_user_mongodb(self,username,password,avatar,token,shop_cookies,shop_id,shop_name):
        #SAI CANNOT CREATE NEW USER, MUST LOCATE username_az and insert new shopee to the shopee list
        newUser = backend.users.User(self,username,password,avatar,token) # Create a blank user firstName
        # Then add shopee information
        newUser.add_new_shopee_shop(shop_cookies,shop_id,shop_name)
        Database_mongoDB.registered_Users_Collection.insert_one(newUser.as_dict())

# x = Database_mongoDB()
# x.connect_to_mongoDB()
# x.registered_Users_Collection.update_one(
#   { '_id': 1 },
#   { '$pull': { 'shopee.0.reply_rating.rating_1star': 'dfsdfsdfsdfsdfdsfsdfsdf'  } }
# )
