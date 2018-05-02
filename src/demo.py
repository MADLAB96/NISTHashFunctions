import keccak
import blakeC
import grostlC

import os
from binascii import hexlify, unhexlify
import binascii
import time
import sys

Msg = raw_input("Input a string to be hashed: ")
msg = bytearray(binascii.hexlify(Msg))
msg = msg[:len(msg)//8]
Msg = Msg[:len(msg)//8]

keccakOut = keccak.Keccak(576, 1024, msg, 0x06, 512//8)
print("-----Keccak Output------")
print(binascii.hexlify(keccakOut))
print("------------------------")

grostlOut = grostlC.groestl(512).digest(Msg)
print("-----Grostl Output------")
print(binascii.hexlify(grostlOut))
print("------------------------")

blakeOut = blakeC.BLAKE(512).digest(Msg)
print("------BLAKE Output------")
print(binascii.hexlify(blakeOut))
print("------------------------")