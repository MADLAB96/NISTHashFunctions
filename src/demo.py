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

t1 = time.time()
keccakOut = keccak.Keccak(576, 1024, msg, 0x06, 512//8)
t2 = time.time()
print("-----Keccak Output------ total time: %f " % (t2-t1))
print(binascii.hexlify(keccakOut))
print("------------------------------------------------")

t1 = time.time()
grostlOut = grostlC.groestl(512).digest(Msg)
t2 = time.time()
print("-----Grostl Output------ total time: %f " % (t2-t1))
print(binascii.hexlify(grostlOut))
print("------------------------------------------------")

t1 = time.time()
blakeOut = blakeC.BLAKE(512).digest(Msg)
t2 = time.time()
print("------BLAKE Output------ total time: %f " % (t2-t1))
print(binascii.hexlify(blakeOut))
print("------------------------------------------------")