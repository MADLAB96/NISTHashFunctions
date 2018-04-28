import keccakC
import os
import binascii


testpath = os.path.abspath(os.path.join('../test/TestVectors'))
verbose=False
fileExt = '.rsp'
files=[
    #filename, r,     c,   d,    n
    ['SHA224', 1152, 448, 0x06, 224],
    ['SHA256', 1088, 512, 0x06, 256],
    ['SHA384', 832, 768, 0x06, 384],
    ['SHA512', 576, 1024, 0x06, 512],
]

sizes=["ShortMsg"]

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
        # testfile = open(os.path.join(testpath, "SHA512ShortMsg.rsp"), 'r')
        print(testfile.name)

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
                    computed = keccakC.Keccak(r, c, msg, d, n//8)
                    #Compare the results
                    if (computed != reference):
                        print('ERROR: \n\t type=%s\n\t length=%d\n\t' % (suffix, Len))
                        # print('ERROR: \n\t type=%s\n\t length=%d\n\t message=%s\n\t reference=%s\n\t computed=%s' % (suffix, Len, Msg, binascii.hexlify(reference), binascii.hexlify(computed)))
                        # exit()
        # print("OK\n")
        # print('OK: \n\t type=%s\n\t length=%d\n\t' % (suffix, Len))
        print('ok: \n\t type=%s\n\t length=%d\n\t message=%s\n\t reference=%s\n\t computed=%s\n' % (suffix, Len, Msg, binascii.hexlify(reference), binascii.hexlify(computed)))
        testfile.close()

