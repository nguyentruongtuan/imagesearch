from flask import Flask, render_template, jsonify, request, json
from search import searchFile, createProduct, searchProduct
from generateHash import genHash
from bson import json_util


def parse_json(data):
    return json.loads(json_util.dumps(data))
  
  
app = Flask(__name__)
# bootstrap = Bootstrap4(app)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/generate", methods=['POST'])
def generate():
    genHash()
    return render_template('index.html')


@app.route("/product", methods=['GET'])
def product():
    product = searchProduct('ssss')
    
    return parse_json({"prouducts": product})


@app.route("/product", methods=['POST'])
def create():
    product = createProduct()
    
    return parse_json({"id": product})


@app.route("/search", methods=['POST'])
def search():

  file = request.get_data()

  tmpPath = './tmp.png'

  f = open(tmpPath, 'wb')
  f.write(file)
  f.close()

  result = searchFile(tmpPath)

  print(result)


  return jsonify(result)


