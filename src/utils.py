import pathlib
from os import path


def getCurrentPath():

    return pathlib.Path(__file__).parent.resolve()


def convert_path(_path):
    _path = _path.split("/")
    return path.join(*_path[_path.index("data")+1:])
    

def map_path(x):

    x["path"] = convert_path(x["path"])
    return x
