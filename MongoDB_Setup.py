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

test = {'hello': 'apple'}

registered_Users_Collection.insert_one(test)

documents = registered_Users_Collection.find({})

for document in documents:
    print(document)