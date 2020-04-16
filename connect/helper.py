import hashlib
import time

header = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36'}


def GetTimeStamp():
    return str(int(time.time() * 1000))


def GetWHUEncode():
    return "%E6%AD%A6%E5%A4%A7%E6%9C%AC%E7%A7%91%E6%95%99%E5%8A%A1%E7%B3%BB%E7%BB%9F"


def EncryptPassword(pwd):
    encrypt = hashlib.md5()
    encrypt.update(pwd.encode("ASCII"))
    return encrypt.hexdigest()
