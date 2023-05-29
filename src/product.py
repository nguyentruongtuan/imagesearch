
import pymongo


CLIENT = pymongo.MongoClient(
    "mongodb://root:123123@localhost:27017/?authSource=admin")
DB = CLIENT["searchimage"]
productCol = DB["product"]


def searchProduct(path):

    productCol = DB["product"]

    products = []

    for p in productCol.find():
        products.append(p)
    # pprint.pprint(products)
    # for p in products:
    #   print(p)

    return products


def createProduct(path='', descriptio='', name=''):
    p = productCol.insert_one({
        "path": path,
        "name": name,
        "description": descriptio
    })

    return p.inserted_id
