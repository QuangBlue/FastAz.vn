import pymongo
import datetime

client = pymongo.MongoClient(
    "mongodb+srv://huy8208:741456963@shopeemastertoolcluster.n4haz.mongodb.net/Shopee_Master_Tool_Database?retryWrites=true&w=majority")

# db = client['Shopee_Master_Tool_Database'] Create a database, if it already exists, skips
# Collection == table
# Create Shopee__Registered_Users Collection
# ShopeeRegisteredUsers = db['Shopee__Registered_Users']


# Get database and collection
db = client.get_database("Shopee_Master_Tool_Database")
registered_Users_Collection = db.get_collection("Shopee__Registered_Users")


def insertDB(data):
    registered_Users_Collection.insert_one(data)


def retrieveDB():
    document = registered_Users_Collection.find({})
    return document

def updateDB(old,new):
    registered_Users_Collection.document.replace_one(old,new)

# data = {"_id":"ABC124",'Name': 'Giày China', 'SKU': '4567', 'Image': 'URL'}
#
# insertDB(data)

everything = retrieveDB()
for elem in everything:
    print(elem)
old = {'Name': 'Giày Adidas'}
data = {'Name':'hang tau chat luong cao'}
updateDB(old,data)

