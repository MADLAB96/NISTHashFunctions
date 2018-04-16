# Keccak Python Implementation

# Constants
n = 24
# Round constants
RC = [  0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
        0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
        0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
        0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
        0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
        0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
        0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
        0x8000000000008080, 0x0000000080000001, 0x8000000080008008 ]

# Rotation Constants
ROTC = [ 1,  3,  6,  10, 15, 21, 28, 36, 45, 55, 2,  14,
         27, 41, 56, 8,  25, 43, 62, 18, 39, 61, 20, 44 ]


# Permutations f-function
def KeccakF1600(state, A):
    # Permutation round-function
    def KeccakRound(A, RC):
        # 0 step
        # ρ and π steps
        # χ step
        # ι step

    for i in range(n):
        A = KeccakRound(A, RC[i])
    return A



# Sponge Functions
def Keccak(state, mbytes, mbits):
    # Padding
    # Initialization
    # Absorbing Phase
    # Squeezing Phase

# State Generation
# r: bitrate
# c: capacity
class State(object):
    W = 5
    H = 5

    def __init__(self, r, c):
        self.r = r
        self.c = class
