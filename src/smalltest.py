import keccak
import os
import binascii


msg = "21"
Len = 8
bytemsg = bytearray(binascii.unhexlify(msg))
bytemsg = bytemsg[:Len//8]
md = "3831a6a6155e509dee59a7f451eb35324d8f8f2df6e3708894740f98fdee23889f4de5adb0c5010dfb555cda77c8ab5dc902094c52de3278f35a75ebc25f093a"
mdmsg = bytearray(binascii.unhexlify(md))

n = len(mdmsg)*8


if ((Len % 8) == 0):
    digest = keccak.Keccak(576, 1024, bytemsg, 0x06, (n//8))
    print("our digest       " + binascii.hexlify(digest))
    print("correct          " + binascii.hexlify(mdmsg))
    if(digest == mdmsg):
        print("OK")
    else:
        print("NOPE")