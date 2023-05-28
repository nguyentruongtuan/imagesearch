from flask import Flask, render_template, request, json, redirect
from search import searchFile
from product import searchProduct, createProduct, searchProductByPath
from generateHash import genHash
from bson import json_util
from flask_bootstrap import Bootstrap4
import os
import pathlib
from utils import convert_path

app = Flask(__name__, static_folder='data')
bootstrap = Bootstrap4(app)


def parse_json(data):
    return json.loads(json_util.dumps(data))


@app.route("/")
def main():
    return render_template('index.html', bootstrap=bootstrap)


@app.route("/product", methods=["GET"])
def product_list():
    products = searchProduct()

    return render_template('product.html', bootstrap=bootstrap, products=products)


@app.route("/create-product", methods=["POST"])
def create_product():

    name = request.form['name']
    description = request.form['description']
    file = request.files['product-image']

    # save file to data path
    currentPath = pathlib.Path(__file__).parent.resolve()
    fullpath = os.path.join(currentPath, 'data', file.filename)
    file.save(fullpath)
    createProduct(name=name, descriptio=description, path=fullpath)

    return redirect('/product')


@app.route("/generate", methods=['POST'])
def generate():
    genHash()
    return redirect('/')


@app.route("/api/product", methods=['GET'])
def product():
    product = searchProduct()

    return parse_json({"prouducts": product})


@app.route("/api/product", methods=['POST'])
def create():
    product = createProduct()

    return parse_json({"id": product})


@app.route("/api/search", methods=['POST'])
def search():

    file = request.get_data()

    tmpPath = './tmp.png'

    f = open(tmpPath, 'wb')
    f.write(file)
    f.close()

    paths = searchFile(tmpPath)
    
    result = searchProductByPath(path=paths[:3])
    
    products = []
    for _path in paths:
        for item in result:
            if item["path"] == convert_path(_path):
                products.append(item)
    
    resultHTML = render_template('result.html', products=products)

    return resultHTML

def getstaticPath(path=''):
    
    return