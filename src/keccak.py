# -*- coding: utf-8 -*-
# Keccak Python Implementation

import os
import base64
import binascii
import io
import sys

# Round constants
RC = [  0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
        0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
        0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
        0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
        0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
        0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
        0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
        0x8000000000008080, 0x0000000080000001, 0x8000000080008008 ]

# rotation offset utility function
def rot(a, n):
    return ((a >> (64-(n%64))) + (a << (n%64))) % (1 << 64)
    # return ((input << offset) ^ (input >> (64-offset)))

def load64(b):
    return sum((b[i] << (8*i)) for i in range(8))

def store64(a):
    return list((a >> (8*i)) % 256 for i in range(8))

# Permutations f-function
# A are the lanes
# B C D are intermediate lane variables
def KeccakF1600Rounds(A):
    # Permutation round-function
    R = 1
    for i in range(24): # 24 rounds
        # 0 step
        C = [A[x][0] ^ A[x][1] ^ A[x][2] ^ A[x][3] ^ A[x][4] for x in range(5)]
        D = [C[(x+4)%5] ^ rot(C[(x+1)%5], 1) for x in range(5)]

        for x in range(5):
            for y in range(5):
                A[x][y] =  A[x][y] ^ D[x]
        # ρ and π steps
        # for x in range(5):
        # for y in range(5):
        #     t = x+y
        #     B[y][(2*x) + (3*y)] = [rot(A[x][y], (t+1)*(t+2)//2) for x in range(5)]
        (x, y) = (1, 0)
        current = A[x][y]
        for t in range(24):
            (x, y) = (y, (2*x+3*y)%5)
            (current, A[x][y]) = (A[x][y], rot(current, (t+1)*(t+2)//2))

        # χ step
        for y in range(5):
            T = [A[x][y] for x in range(5)]
            for x in range(5):
                A[x][y] = T[x] ^(~(T[(x+1)%5]) & (T[(x+2)%5]))
        
        # ι step
        A[0][0] = A[0][0] ^ RC[i]

    return A

def KeccakF1600(S):
    lanes = [[load64(S[8*(x+5*y):8*(x+5*y)+8]) for y in range(5)] for x in range(5)]
    lanes = KeccakF1600Rounds(lanes)
    S = bytearray(200)
    for x in range(5):
        for y in range(5):
            S[8*(x+5*y):8*(x+5*y)+8] = store64(lanes[x][y])
    return S

# Sponge Functions
# r: bitrate
# c: capacity
# d: delimited suffix
# S: state
def Keccak(r, c, input, d, outputLen):
    # Initialization
    outputBytes = bytearray()
    rateInBytes = r//8 #integer division to set rate to bytes
    blockSize = 0
    inputOffset = 0
    if (((r + c) != 1600) or ((r % 8) != 0)):
        return
    S = bytearray([0 for i in range(200)]) # State initialization

    # Absorbing Phase
    while(inputOffset < len(input)):
        blockSize = min(len(input)-inputOffset, rateInBytes)
        for i in range(blockSize):
            S[i] = S[i] ^ input[i+inputOffset]
        inputOffset = inputOffset + blockSize
        if (blockSize == rateInBytes):
            S = KeccakF1600(S)
            blockSize = 0

    # Padding
    S[blockSize] = S[blockSize] ^ d
    if (((d & 0x80) != 0) and (blockSize == (rateInBytes-1))):
        S = KeccakF1600(S)
    S[rateInBytes-1] = S[rateInBytes-1] ^ 0x80
    S = KeccakF1600(S)
    
    # Squeezing Phase
    while(outputLen > 0):
        blockSize = min(outputLen, rateInBytes)
        outputBytes = outputBytes + S[0:blockSize]
        outputLen = outputLen - blockSize
        if (outputLen > 0):
            S = KeccakF1600(S)
    return outputBytes

def SHA3_224(input):
    return Keccak(1152, 448, input, 0x06, 224//8)

def SHA3_256(input):
    return Keccak(1088, 512, input, 0x06, 256//8)

def SHA3_384(input):
    return Keccak(832, 768, input, 0x06, 384//8)

def SHA3_512(input):
    return Keccak(576, 1024, input, 0x06, 512//8)
# -*- coding: utf-8 -*-
# Implementation by Gilles Van Assche, hereby denoted as "the implementer".

# For more information, feedback or questions, please refer to our website:
# https://keccak.team/

# To the extent possible under law, the implementer has waived all copyright
# and related or neighboring rights to the source code in this file.
# http://creativecommons.org/publicdomain/zero/1.0/

# def ROL64(a, n):
#     return ((a >> (64-(n%64))) + (a << (n%64))) % (1 << 64)

# def KeccakF1600onLanes(lanes):
#     R = 1
#     for round in range(24):
#         # θ
#         C = [lanes[x][0] ^ lanes[x][1] ^ lanes[x][2] ^ lanes[x][3] ^ lanes[x][4] for x in range(5)]
#         D = [C[(x+4)%5] ^ ROL64(C[(x+1)%5], 1) for x in range(5)]
#         lanes = [[lanes[x][y]^D[x] for y in range(5)] for x in range(5)]
#         # ρ and π
#         (x, y) = (1, 0)
#         current = lanes[x][y]
#         for t in range(24):
#             (x, y) = (y, (2*x+3*y)%5)
#             (current, lanes[x][y]) = (lanes[x][y], ROL64(current, (t+1)*(t+2)//2))
#         # χ
#         for y in range(5):
#             T = [lanes[x][y] for x in range(5)]
#             for x in range(5):
#                 lanes[x][y] = T[x] ^((~T[(x+1)%5]) & T[(x+2)%5])
#         # ι
#         for j in range(7):
#             R = ((R << 1) ^ ((R >> 7)*0x71)) % 256
#             if (R & 2):
#                 lanes[0][0] = lanes[0][0] ^ (1 << ((1<<j)-1))
#     return lanes

