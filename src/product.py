from db import DB
from utils import getCurrentPath, map_path


productCol = DB["product"]





def searchProduct():

    productCol = DB["product"]

    products = []

    for p in productCol.find().sort("_id"):
        products.append(p)

    products = map(map_path, products)

    return products


def searchProductByPath(path=[]):

    productCol = DB["product"]

    products = []

    for p in productCol.find({"path": {"$in": path}}):
        products.append(p)

    products = map(map_path, products)

    return products


def createProduct(path='', descriptio='', name=''):
    p = productCol.insert_one({
        "path": path,
        "name": name,
        "description": descriptio
    })

    return p.inserted_id
