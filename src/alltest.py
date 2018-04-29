import keccak
import blakeC
import os
from binascii import hexlify, unhexlify
import binascii

# testpath = os.path.abspath(os.path.join('../test/shabytetestvectors'))
testpath = os.path.abspath(os.path.join('../test/SHA-3Bit'))
verbose=False
fileExt = '.rsp'
files=[
    #filename, r,     c,   d,    n
    ['SHA3_224', 1152, 448, 0x06, 224],
    ['SHA3_256', 1088, 512, 0x06, 256],
    ['SHA3_384', 832, 768, 0x06, 384],
    ['SHA3_512', 576, 1024, 0x06, 512],
]

sizes=["ShortMsg", "LongMsg"]


# Testing Keccak: 
print("Keccak Testing")
for file in files:
    suffix = file[0]
    r = file[1]
    c = file[2]
    d = file[3]
    n = file[4]
    for size in sizes:
        # print('Processing file: %sMsgKAT_%s.txt...' % (size, file[0]))
        # print("Keccak[r=%d, c=%d] with '%s' suffix" % (file[1], file[2], file[3])
        extrapath = suffix + size + fileExt    
        testfile = open(os.path.join(testpath, extrapath), 'r')
        # testfile=open(os.path.join(testpath,size+('MsgKAT_%s.txt' % suffix)), 'r')
        
        # print(testfile.name)

        for line in testfile:
            if line.startswith('Len'):
                Len=int(line.split(' = ')[1].strip('\n\r'))
            if line.startswith('Msg'):
                Msg=line.split(' = ')[1].strip('\n\r')
                msg = bytearray(binascii.unhexlify(Msg))
                msg = msg[:Len//8]
            if (line.startswith('MD')):
                MD_ref=line.split(' = ')[1].strip('\n\r')
                reference = bytearray(binascii.unhexlify(MD_ref))
                # If line starts with 'Squeezed', use the output length from the test vector
                if line.startswith('Squeezed'):
                    n = len(reference)*8
                elif n == 0:
                    print("Error: the output length should be specified")
                    exit()

                if ((Len % 8) == 0):
                    # Perform our own computation
                    computed = keccak.Keccak(r, c, msg, d, n//8)
                    #Compare the results
                    if (computed != reference):
                        print('ERROR: \n\t type=%s\n\t length=%d\n\t' % (suffix, Len))
                        # print('ERROR: \n\t type=%s\n\t length=%d\n\t message=%s\n\t reference=%s\n\t computed=%s' % (suffix, Len, Msg, binascii.hexlify(reference), binascii.hexlify(computed)))
                        exit()
                                            
        testfile.close()
print("OK\n")
    
# Testing Skein
# Testing JH
# Testing Grostl
# Testing BLAKE
print("BLAKE Testing")

def test_BLAKE(hashlen, msg, expect):
    print('      BLAKE-%d:  msg = %s  length = %d' % 
                        (hashlen, msg.decode(), len(msg)))
    digest = blakeC.BLAKE(hashlen).digest(msg)
    print('        %s %s' % ('valid    ' if digest == unhexlify(expect)
                                else 'ERROR >>>', hexlify(digest).decode()))

msg = b'Kilroy was here!'
hashlen = 224
expect = (b'4504cb0314fb2a4f7a692e696e487912' +
                  b'fe3f2468fe312c73a5278ec5')
test_BLAKE(hashlen, msg, expect)
# print('ERROR: \n\t type=%s\n\t length=%d\n\t message=%s\n\t reference=%s\n\t computed =%s' % (suffix, hashlen, Msg, (reference), binascii.hexlify(computed)))



#Compare the results
# if (computed != reference):
#     # print('ERROR: \n\t type=%s\n\t length=%d\n\t' % (suffix, Len))
#     print('ERROR: \n\t type=%s\n\t length=%d\n\t message=%s\n\t reference=%s\n\t computed =%s' % (suffix, hashlen, Msg, (reference), binascii.hexlify(computed)))
#     exit()
# for file in files:
#     suffix = file[0]
#     r = file[1]
#     c = file[2]
#     d = file[3]
#     n = file[4]
#     for size in sizes:
#         # print('Processing file: %sMsgKAT_%s.txt...' % (size, file[0]))
#         # print("Keccak[r=%d, c=%d] with '%s' suffix" % (file[1], file[2], file[3])
#         extrapath = suffix + size + fileExt    
#         testfile = open(os.path.join(testpath, extrapath), 'r')
#         # testfile=open(os.path.join(testpath,size+('MsgKAT_%s.txt' % suffix)), 'r')
        
#         # print(testfile.name)

#         for line in testfile:
#             if line.startswith('Len'):
#                 Len=int(line.split(' = ')[1].strip('\n\r'))
#             if line.startswith('Msg'):
#                 Msg=line.split(' = ')[1].strip('\n\r')
#                 msg = bytearray(binascii.unhexlify(Msg))
#                 msg = msg[:Len//8]
#             if (line.startswith('MD')):
#                 MD_ref=line.split(' = ')[1].strip('\n\r')
#                 reference = bytearray(binascii.unhexlify(MD_ref))
#                 # If line starts with 'Squeezed', use the output length from the test vector
#                 if line.startswith('Squeezed'):
#                     n = len(reference)*8
#                 elif n == 0:
#                     print("Error: the output length should be specified")
#                     exit()

#                 if ((Len % 8) == 0):
#                     # Perform our own computation
#                     computed = blakeC.BLAKE(n).digest(msg)
#                     #Compare the results
#                     if (computed != reference):
#                         # print('ERROR: \n\t type=%s\n\t length=%d\n\t' % (suffix, Len))
#                         print('ERROR: \n\t type=%s\n\t length=%d\n\t message=%s\n\t reference=%s\n\t computed =%s' % (suffix, Len, Msg, binascii.hexlify(reference), binascii.hexlify(computed)))
#                         exit()
                                            
#         testfile.close()
# print("OK\n")
 