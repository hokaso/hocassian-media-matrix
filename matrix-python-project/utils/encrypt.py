# -*- coding: utf-8 -*-
# AES-demo #采用AES对称加密算法
import os, json, time, base64
from Crypto.Cipher import AES


def add_to_16(value):
    while len(value) % 16 != 0:
        value += '\0'

    return str.encode(value)


# 加密方法
def encrypt():

    with open("../key.txt", 'r') as f:
        key = f.readline()

    with open("list.txt", "r") as f0:
        _info = f0.readlines()

    info = [i.replace("\n", "") for i in _info]

    for ikey in info:
        with open(ikey, "rb") as f1:
            info = f1.read()

        aes = AES.new(add_to_16(key), AES.MODE_ECB)
        encrypt_aes = aes.encrypt(add_to_16(str(info)))
        encrypted_text = str(base64.encodebytes(encrypt_aes), encoding='cp936')

        with open(ikey + ".en", 'w') as f1:
            f1.write(encrypted_text)

if __name__ == '__main__':
    encrypt()
