from PIL import Image
from hashImage import convert_hash
from hashImage import hamming
from hashImage import dhash
from imutils import paths
import pickle
import vptree
import cv2
import pathlib
import os 

def genHash():
  
	currentPath = pathlib.Path(__file__).parent.resolve()
	imgDir = '{}/dist'.format(currentPath)
	if not os.path.exists(imgDir):
		os.makedirs(imgDir)

	imagePaths = list(paths.list_images('{}/data'.format(currentPath)))
	hashes = {}

	for (i, imagePath) in enumerate(imagePaths):
		# load the input image
		print("[INFO] processing image {}/{}".format(i + 1,
																								len(imagePaths)))
		image = cv2.imread(imagePath)
		# compute the hash for the image and convert it
		h = dhash(image)
		h = convert_hash(h)
		# update the hashes dictionary
		l = hashes.get(h, [])
		l.append(imagePath)
		hashes[h] = l


	print("[INFO] building VP-Tree...")
	points = list(hashes.keys())
	tree = vptree.VPTree(points, hamming)


	print("[INFO] serializing VP-Tree...")
	f = open('{}/tree.pickle'.format(imgDir), "wb")
	f.write(pickle.dumps(tree))
	f.close()


	# serialize the hashes to dictionary
	print("[INFO] serializing hashes...")
	f = open('{}/hashes.pickle'.format(imgDir), "wb")
	f.write(pickle.dumps(hashes))
	f.close()


# print(tree)
