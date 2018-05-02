import keccak
import blakeC
import grostlC

import os
from binascii import hexlify, unhexlify
import binascii
import time
import sys

# testpath = os.path.abspath(os.path.join('../test/TestVectors'))
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

sizes=["ShortMsg"]

of = open('output.txt', 'w')
of.write('Keccak:\n')

total = 0.0
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
        of.write('%s:%s\n' % (suffix, size))
        
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
                    t1 = time.time()
                    computed = keccak.Keccak(r, c, msg, d, n//8)
                    t2 = time.time()
                    # print("TIME of %s: %f" % (suffix, (t2-t1)))       
                    total += (t2-t1)
                    of.write('%f\n' % (t2-t1))
                                            
        testfile.close()
print("OK -- %f\n" % (total))
of.write('Keccak total: %f\n' % total)

# Testing Skein
# print("Skein Testing")
# total = 0.0
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
#                     t1 = time.time()                    
#                     computed = grostlC.groestl(n).digest(Msg)
#                     t2 = time.time()
#                     # print("TIME of %s: %f" % (suffix, (t2-t1))) 
#                     total += (t2-t1)             
                    
#                     # Compare the results
#                     # if (computed != reference):
#                         # print('ERROR: type=%s length=%d' % (suffix, Len))
#                         # print('ERROR: type=%s length=%d\n\t message=%s\n\t reference=%s\n\t computed =%s' % (suffix, Len, Msg, binascii.hexlify(reference), binascii.hexlify(computed)))
#                         # exit()
#                     # else: 
#                         # print('OK: \n\t type=%s\n\t length=%d\n\t' % (suffix, Len))
                        
                                            
#         testfile.close()
# print("OK -- %f\n" % (total))
# Testing JH
# print("JH Testing")
# total = 0.0

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
#                 # msg = bytearray(binascii.unhexlify(Msg))
#                 msg = Msg[:Len//8]
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
#                     t1 = time.time()
#                     computed = jh.hashbits(n, msg)
#                     t2 = time.time()
#                     # print("TIME of %s: %f" % (suffix, (t2-t1)))       
#                     total += (t2-t1)             
#                     #Compare the results
#                 # if (computed != reference):
#                 #     print('ERROR: \n\t type=%s\n\t length=%d\n\t' % (suffix, Len))
#                 #     print('ERROR: \n\t type=%s\n\t length=%d\n\t message=%s\n\t reference=%s\n\t computed=%s' % (suffix, Len, Msg, binascii.hexlify(reference), binascii.hexlify(computed)))
#                 #     exit()
                                            
#         testfile.close()
# print("OK -- %f\n" % (total))

# Testing Grostl
print("Grostl Testing")
of.write('Grostl:\n')

total = 0.0
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
        of.write('%s:%s\n' % (suffix, size))

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
                    t1 = time.time()                    
                    computed = grostlC.groestl(n).digest(Msg)
                    t2 = time.time()
                    # print("TIME of %s: %f" % (suffix, (t2-t1))) 
                    total += (t2-t1)             
                    of.write('%f\n' % (t2-t1))                        
                                            
        testfile.close()
print("OK -- %f\n" % (total))
of.write('Grostl total: %f\n\n' % total)
 
# Testing BLAKE
print("BLAKE Testing")
of.write('BLADE:\n')
total = 0.0
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
        of.write('%s:%s\n' % (suffix, size))

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
                    t1 = time.time()                    
                    computed = blakeC.BLAKE(n).digest(msg)
                    t2 = time.time()
                    # print("TIME of %s: %f" % (suffix, (t2-t1))) 
                    total += (t2-t1)             
                    of.write('%f\n' % (t2-t1))                        
                                            
        testfile.close()
print("OK -- %f\n" % (total))
of.write('BLAKE total: %f\n' % total)

of.close()
