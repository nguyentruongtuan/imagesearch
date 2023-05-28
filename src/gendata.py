import requests
from bs4 import BeautifulSoup


def getDataFromURL(url):
    req = requests.get(url)
    content = BeautifulSoup(req.content, 'html.parser')
