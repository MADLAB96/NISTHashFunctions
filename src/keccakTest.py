import keccak
import os
import binascii


msg = "35250c62af89a681d1ec"
Len = 78
bytemsg = bytearray(binascii.unhexlify(msg))
bytemsg = bytemsg[:Len//8]
md = "fd93f50f48eb2d96e290c79d209c5c9abeee02c164044e791ae8e3f6b015076f817083b74e2cf60a9e7413a472802ed82b048f248fcf85c2d1fc41834b0a3d40"
mdmsg = bytearray(binascii.unhexlify(md))
digest = keccak.SHA3_512(bytemsg)
print("our digest " + binascii.hexlify(digest))
print("correct    " + binascii.hexlify(mdmsg))
if(digest == md):
    print("true")