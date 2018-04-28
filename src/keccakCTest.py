import binascii
import keccakC
import keccak
import os

dirTestVector=os.path.abspath(os.path.join('../test/TestVectors'))
verbose=False
instances=[
    ['SHAKE128', 1344, 256, 0x1F, 0],
    ['SHAKE256', 1088, 512, 0x1F, 0],
    ['SHA3-224', 1152, 448, 0x06, 224],
    ['SHA3-256', 1088, 512, 0x06, 256],
    ['SHA3-384', 832, 768, 0x06, 384],
    ['SHA3-512', 576, 1024, 0x06, 512],
]
fileTypes=['Short']

def delimitedSuffixInBinary(delimitedSuffix):
    binary = ''
    while(delimitedSuffix != 1):
        binary = binary + ('%d' % (delimitedSuffix%2))
        delimitedSuffix = delimitedSuffix//2

for instance in instances:
    [fileNameSuffix, r, c, delimitedSuffix, n] = instance
    for fileType in fileTypes:
        print('Processing file: %sMsgKAT_%s.txt...' % (fileType, fileNameSuffix))
        print("Keccak[r=%d, c=%d] with '%s' suffix" % (r, c, delimitedSuffixInBinary(delimitedSuffix)))

        #Open the corresponding file
        try:
            referenceFile=open(os.path.join(dirTestVector,fileType+('MsgKAT_%s.txt' % fileNameSuffix)), 'r')
        except IOError:
            print("Error: test vector files must be stored in %s" % (dirTestVector))
            exit()

        #Parse the document line by line (works only for Short and Long files)
        for line in referenceFile:
            if line.startswith('Len'):
                Len=int(line.split(' = ')[1].strip('\n\r'))
            if line.startswith('Msg'):
                Msg=line.split(' = ')[1].strip('\n\r')
                msg = bytearray(binascii.unhexlify(Msg))
                msg = msg[:Len//8]
            if (line.startswith('MD') or line.startswith('Squeezed')):
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
                    computed1 = keccakC.Keccak(r, c, msg, delimitedSuffix, n//8)
                    computed2 = keccak.Keccak(r, c, msg, delimitedSuffix, n//8)
                    #Compare the results
                    if (computed2 != reference):
                        print('ERROR: \n\t type=%s\n\t length=%d\n\t message=%s\n\t reference=%s\n\t computed1=%s' % (fileNameSuffix, Len, Msg, binascii.hexlify(reference), binascii.hexlify(computed)))
                        exit()

        print("OK\n")
        referenceFile.close()