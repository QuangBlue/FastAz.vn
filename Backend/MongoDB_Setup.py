import pymongo
import datetime
import Backend.users as userClass
# What does this mongoDB do?
# update one document
# update multiple documents
# insert one document
# insert multiple documents

# client = pymongo.MongoClient("mongodb+srv://quang_db:Thangkhung123@cluster0.cv2te.mongodb.net/shopee_db?retryWrites=true&w=majority")
# db = client['Shopee_Master_Tool_Database'] Create a database, if it already exists, skips
# Collection == table
# Create Shopee__Registered_Users Collection
# ShopeeRegisteredUsers = db['Shopee__Registered_Users']
# Get database and collection
# db = client.get_database("shopee_db")
# registered_Users_Collection = db.get_collection("user_db")


client = pymongo.MongoClient(
    "mongodb+srv://huy8208:741456963@shopeemastertoolcluster.n4haz.mongodb.net/Shopee_Master_Tool_Database?retryWrites=true&w=majority")
with client:
    db = client.get_database("Shopee_Master_Tool_Database")
    registered_Users_Collection = db.get_collection("Shopee__Registered_Users")




def find_and_updateDB(ids, data):
    registered_Users_Collection.find_one_and_update(
        {"_id": ids},
        {"$set": data},
        upsert=True  # Set True se tao moi khi khong co du lieu
    )


def update_one(old_data,
               new_data):  # Hàm này để update theo logic và áp dụng cho update hàng loạt qua hàm for. Từ old_data sẽ tìm và đổi thành giá trị new_data cho kết quả find đầu tiên.

    registered_Users_Collection.update_one(
        {old_data}, {"$set":
                         {new_data}
                     }
    )


def check_username_fastaz(username):
    if registered_Users_Collection.count_documents({"Username_fastAZ":username}) != 0:
        return True
    else:
        return False

def insert_new_user_mongodb(username, password, avatar,token):
    newUser = userClass.User(username,password,avatar,token)
    registered_Users_Collection.insert_one(newUser.as_dict())

# data = {"_id": "ABC123", 'Name': 'Giày China', 'SKU': '4567', 'Image': 'URL'}

# user1 = User(username="Huy", password="yes", avatar="img1234")
# user1.add_new_product(115, "Giày xịn", 1000, "img_")

# insertDB(user1.as_dict())

