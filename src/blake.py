# Constants for BLAKE

#BLAKE-512
IV64 = [
    0x6A09E667F3BCC908, 0xBB67AE8584CAA73B,
    0x3C6EF372FE94F82B, 0xA54FF53A5F1D36F1,
    0x510E527FADE682D1, 0x9B05688C2B3E6C1F,
    0x1F83D9ABFB41BD6B, 0x5BE0CD19137E2179,
]

#BLAKE-384
IV48 = [
    0xCBBB9D5DC1059ED8, 0x629A292A367CD507,
    0x9159015A3070DD17, 0x152FECD8F70E5939,
    0x67332667FFC00B31, 0x8EB44A8768581511,
    0xDB0C2E0D64F98FA7, 0x47B5481DBEFA4FA4,
]

# note: the values here are the same as the high-order 
#       half-words of IV64
#BLAKE-256
IV32 = [
    0x6A09E667, 0xBB67AE85,
    0x3C6EF372, 0xA54FF53A,
    0x510E527F, 0x9B05688C,
    0x1F83D9AB, 0x5BE0CD19,
]

# note: the values here are the same as the low-order 
#       half-words of IV48
#BLAKE-224
IV28 = [
    0xC1059ED8, 0x367CD507,
    0x3070DD17, 0xF70E5939,
    0xFFC00B31, 0x68581511,
    0x64F98FA7, 0xBEFA4FA4,
]

# constants for BLAKE-512 and BLAKE-256
C64 = [
    0x243F6A8885A308D3, 0x13198A2E03707344,
    0xA4093822299F31D0, 0x082EFA98EC4E6C89,
    0x452821E638D01377, 0xBE5466CF34E90C6C,
    0xC0AC29B7C97C50DD, 0x3F84D5B5B5470917,
    0x9216D5D98979FB1B, 0xD1310BA698DFB5AC,
    0x2FFD72DBD01ADFB7, 0xB8E1AFED6A267E96,
    0xBA7C9045F12C7F99, 0x24A19947B3916CF7,
    0x0801F2E2858EFC16, 0x636920D871574E69,
]

# constants for BLAKE-32 and BLAKE-28
# note: concatenate and the values are the same as the values 
#       for the 1st half of C64
C32 = [
    0x243F6A88, 0x85A308D3,
    0x13198A2E, 0x03707344,
    0xA4093822, 0x299F31D0,
    0x082EFA98, 0xEC4E6C89,
    0x452821E6, 0x38D01377,
    0xBE5466CF, 0x34E90C6C,
    0xC0AC29B7, 0xC97C50DD,
    0x3F84D5B5, 0xB5470917,
]

# the 10 permutations of:0,...15}
SIGMA = [
    [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15],
    [14,10, 4, 8, 9,15,13, 6, 1,12, 0, 2,11, 7, 5, 3],
    [11, 8,12, 0, 5, 2,15,13,10,14, 3, 6, 7, 1, 9, 4],
    [ 7, 9, 3, 1,13,12,11,14, 2, 6, 5,10, 4, 0,15, 8],
    [ 9, 0, 5, 7, 2, 4,10,15,14, 1,11,12, 6, 8, 3,13],
    [ 2,12, 6,10, 0,11, 8, 3, 4,13, 7, 5,15,14, 1, 9],
    [12, 5, 1,15,14,13, 4,10, 0, 7, 6, 3, 9, 2, 8,11],
    [13,11, 7,14,12, 1, 3, 9, 5, 0,15, 4, 8, 6, 2,10],
    [ 6,15,14, 9,11, 3, 0, 8,12, 2,13, 7, 1, 4,10, 5],
    [10, 2, 8, 4, 7, 6, 1, 5,15,11, 9,14, 3,12,13, 0],
    [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15],
    [14,10, 4, 8, 9,15,13, 6, 1,12, 0, 2,11, 7, 5, 3],
    [11, 8,12, 0, 5, 2,15,13,10,14, 3, 6, 7, 1, 9, 4],
    [ 7, 9, 3, 1,13,12,11,14, 2, 6, 5,10, 4, 0,15, 8],
    [ 9, 0, 5, 7, 2, 4,10,15,14, 1,11,12, 6, 8, 3,13],
    [ 2,12, 6,10, 0,11, 8, 3, 4,13, 7, 5,15,14, 1, 9],
    [12, 5, 1,15,14,13, 4,10, 0, 7, 6, 3, 9, 2, 8,11],
    [13,11, 7,14,12, 1, 3, 9, 5, 0,15, 4, 8, 6, 2,10],
    [ 6,15,14, 9,11, 3, 0, 8,12, 2,13, 7, 1, 4,10, 5],
    [10, 2, 8, 4, 7, 6, 1, 5,15,11, 9,14, 3,12,13, 0],
]
    


class blake(object):
    #class init method
    #hashlen is in [512, 384, 256, 224]
    def __init__(self, hashlen):
        self.hashlen = hashlen
        self.h     = [0]*8  # current chain value (initialized to the IV)
        self.t     = 0      # number of *BITS* hashed so far
        self.cache = b''    # cached leftover data not yet compressed
        self.salt  = [0]*4  # salt (null by default)
        self.state = 1      # set to 2 by update and 3 by final
        self.nullt = 0      # Boolean value for special case \ell_i=0

        if (hashlen == 224) or (hashlen == 256):
            # setup for 32-bit words and 64-bit block
            # self.byte2int  = self._fourByte2int
            # self.int2byte  = self._int2fourByte
            self.MASK      = 0xFFFFFFFF
            self.WORDBYTES = 4
            self.WORDBITS  = 32
            self.BLKBYTES  = 64
            self.BLKBITS   = 512
            self.ROUNDS    = 14     # was 10 before round 3
            self.cxx  = C32
            self.rot1 = 16          # num bits to shift in G
            self.rot2 = 12          # num bits to shift in G 
            self.rot3 = 8           # num bits to shift in G 
            self.rot4 = 7           # num bits to shift in G
            self.mul  = 0   # for 32-bit words, 32<<self.mul where self.mul = 0
            
            # 224- and 256-bit versions (32-bit words)
            if hashlen == 224:
                self.h = IV28[:]
            else:
                self.h = IV32[:]
    
        elif (hashlen == 384) or (hashlen == 512):
            # setup for 64-bit words and 128-bit block
            # self.byte2int  = self._eightByte2int
            # self.int2byte  = self._int2eightByte
            self.MASK      = 0xFFFFFFFFFFFFFFFF
            self.WORDBYTES = 8
            self.WORDBITS  = 64
            self.BLKBYTES  = 128
            self.BLKBITS   = 1024
            self.ROUNDS    = 16     # was 14 before round 3
            self.cxx  = C64
            self.rot1 = 32          # num bits to shift in G
            self.rot2 = 25          # num bits to shift in G
            self.rot3 = 16          # num bits to shift in G
            self.rot4 = 11          # num bits to shift in G
            self.mul  = 1   # for 64-bit words, 32<<self.mul where self.mul = 1
            
            # 384- and 512-bit versions (64-bit words)
            if hashlen == 384:
                self.h = IV48[:]
            else:
                self.h = IV64[:]
    #digest method
    def digest(msg):

