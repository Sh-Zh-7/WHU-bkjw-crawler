import json
import hashlib
from io import BytesIO
from matplotlib.pyplot import imread

def Json2Dict(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

def Bin2Img(bin_obj):
    return imread(BytesIO(bin_obj), "jpeg")

def EncryptPassword(pwd):
    encrypt = hashlib.md5()
    encrypt.update(pwd.encode("ASCII"))
    return encrypt.hexdigest()
