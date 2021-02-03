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
    registered_Users_Collection = None
    def __init__(self):
        # self.client = None
        # self.db = None
        # self.registered_Users_Collection = None
        self.client = pymongo.MongoClient(
        "mongodb+srv://huy8208:741456963@shopeemastertoolcluster.n4haz.mongodb.net/Shopee_Master_Tool_Database?retryWrites=true&w=majority")
        try: 
            self.db = self.client.get_database("Shopee_Master_Tool_Database")
            Database_mongoDB.registered_Users_Collection = self.db.get_collection("Shopee__Registered_Users")
        except pymongo.errors.ConnectionFailure as error:
            print(str(error))
            exit()
        finally:
            print("Connecting to database sucessfully !!!")  
            
    # def connect(self):
    #     self.client = pymongo.MongoClient(
    #     "mongodb+srv://huy8208:741456963@shopeemastertoolcluster.n4haz.mongodb.net/Shopee_Master_Tool_Database?retryWrites=true&w=majority")
    #     try: 
    #         self.db = self.client.get_database("Shopee_Master_Tool_Database")
    #         self.registered_Users_Collection = self.db.get_collection("Shopee__Registered_Users")
    #     except pymongo.errors.ConnectionFailure as error:
    #         print(str(error))
    #         exit()
    #     finally:
    #         print("Connecting to database sucessfully !!!")  
            
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

    def insert_new_user_mongodb(self,username, password, avatar,token):
        newUser = backend.users.User(username,password,avatar,token)
        Database_mongoDB.registered_Users_Collection.insert_one(newUser.as_dict())


