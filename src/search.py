from hashImage import convert_hash
from hashImage import dhash
import argparse
import pickle
import time
import cv2 
import pathlib
import os
import pymongo
import pprint


CLIENT = pymongo.MongoClient(
    "mongodb://root:123123@db:27017/?authSource=admin")
DB = CLIENT["searchimage"]


def searchProduct(path):
  
  productCol = DB["product"]
  
  products = []
  
  for p in productCol.find():
    products.append(p)
  # pprint.pprint(products)
  # for p in products:
  #   print(p)
  
  return products

def createProduct():
  
  productCol = DB["product"]
  
  p = productCol.insert_one({
   "path": "1",
   "name": "222"
  })
  
  return p.inserted_id 
  


def searchFile(imgPath, disance=30):
  currentPath = pathlib.Path(__file__).parent.resolve()
  print("[INFO] loading VP-Tree and hashes...")
  
  treePath = '{}/dist/tree.pickle'.format(currentPath)
  hashPath = '{}/dist/hashes.pickle'.format(currentPath)
  
  tree = pickle.loads(open(treePath, "rb").read())
  hashes = pickle.loads(open(hashPath, "rb").read())
  # load the input query image
  image = cv2.imread(imgPath)
  # cv2.imshow("Query", image)
  # compute the hash for the query image, then convert it
  queryHash = dhash(image)
  queryHash = convert_hash(queryHash)


  print("[INFO] performing search...")
  start = time.time()
  results = tree.get_all_in_range(queryHash, disance)
  results = sorted(results)
  end = time.time()
  print("[INFO] search took {} seconds".format(end - start))


  paths = []  

  for (d, h) in results:
    # grab all image paths in our dataset with the same hash
    resultPaths = hashes.get(h, [])
    print("[INFO] {} total image(s) with d: {}, h: {}".format(
      len(resultPaths), d, h))
    # loop over the result paths
    for resultPath in resultPaths:
      paths.append(resultPath)
      # load the result image and display it to our screen
      # result = cv2.imread(resultPath)
      # cv2.imshow("Result", result)
      # cv2.waitKey(0)
  return paths