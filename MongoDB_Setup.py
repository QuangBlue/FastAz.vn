import pymongo
import datetime

client = pymongo.MongoClient("mongodb+srv://huy8208:741456963@shopeemastertoolcluster.n4haz.mongodb.net/Shopee_Master_Tool_Database?retryWrites=true&w=majority")
# client = pymongo.MongoClient("mongodb+srv://quang_db:Thangkhung123@cluster0.cv2te.mongodb.net/shopee_db?retryWrites=true&w=majority")


# db = client['Shopee_Master_Tool_Database'] Create a database, if it already exists, skips
# Collection == table
# Create Shopee__Registered_Users Collection
# ShopeeRegisteredUsers = db['Shopee__Registered_Users']


# Get database and collection
# db = client.get_database("shopee_db")
# registered_Users_Collection = db.get_collection("user_db")
db = client.get_database("Shopee_Master_Tool_Database")
registered_Users_Collection = db.get_collection("Shopee__Registered_Users")


def insertDB(data):
    registered_Users_Collection.insert_one(data)


def retrieveDB():
    document = registered_Users_Collection.find({})
    return document

def find_and_updateDB(ids,data):

    registered_Users_Collection.find_one_and_update(
        {"_id" : ids},
        {"$set": data},
        upsert=True # Set True se tao moi khi khong co du lieu
    )

def update_one(old_data,new_data): # Hàm này để update theo logic và áp dụng cho update hàng loạt qua hàm for. Từ old_data sẽ tìm và đổi thành giá trị new_data cho kết quả find đầu tiên.

    registered_Users_Collection.update_one(
        {old_data}, {"$set":
            {new_data } 
        }
    ) 


# data = {"_id":"ABC123",'Name': 'Giày China', 'SKU': '4567', 'Image': 'URL'}
# insertDB(data)

# everything = retrieveDB()
# for elem in everything:
#     print(elem)
# ids = "ABC123"
# data = {'Name':'hang tau chat luong cao'}
# updateDB(ids,data)

