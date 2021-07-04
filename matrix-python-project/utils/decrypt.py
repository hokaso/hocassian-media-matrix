# -*- coding: utf-8 -*-
# AES-demo #采用AES对称加密算法
import os, json, time, base64
from Crypto.Cipher import AES


# str不是16的倍数那就补足为16的倍数
def add_to_16(value):

    while len(value) % 16 != 0:
        value += '\0'

    return str.encode(value)

# 解密方法
def decrypt():

    with open("../key.txt", 'r') as f:
        key = f.readline()

    with open("list.txt", "r") as f0:
        _info = f0.readlines()

    info = [i.replace("\n", "") for i in _info]

    for ikey in info:

        with open(ikey + ".en", "r") as f1:
            text = f1.read()

        aes = AES.new(add_to_16(key), AES.MODE_ECB)
        base64_decrypted = base64.decodebytes(text.encode(encoding='cp936'))
        _decrypted_text = str(aes.decrypt(base64_decrypted), encoding='gbk').replace('\0', '')
        decrypted_text = eval(_decrypted_text)

        with open(ikey, 'wb') as f2:
            f2.write(decrypted_text)


if __name__ == '__main__':
    decrypt()
