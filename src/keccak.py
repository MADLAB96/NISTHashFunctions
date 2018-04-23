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
def rot(input, offset):
    return ((input << offset) ^ (input >> (64-offset)))

# Permutations f-function
# A are the lanes
# B C D are intermediate lane variables
def KeccakF1600(A):
    # Permutation round-function
    for i in range(24): # 24 rounds
        # 0 step
        C = [] 
        D = []
        B = []
        for x in range(5):
            C[x] = A[x][0] ^  A[x][1] ^  A[x][2] ^  A[x][3] ^ A[x][4]   
        for x in range(5):
            D[x] = C[(x+4)%5] ^ rot(C[(x+1)%5], 1)
        for x in range(5):
            for y in range(5):
                A[x][y] =  A[x][y] ^ D[x]
        # ρ and π steps
        for x in range(5):
            for y in range(5):
                t = x+y
                B[y][(2*x) + (3*y)] = rot(A[x][y], (t+1)*(t+2)//2)
        # χ step
        for y in range(5):
            T = [B[x][y] for x in range(5)]
            for x in range(5):
                A[x][y] = T[x] ^(~(T[(x+1)%5]) & (T[(x+2)%5]))
        # ι step
        A[0][0] = A[0][0] ^ RC[i]

    return A

# Sponge Functions
# r: bitrate
# c: capacity
# d: delimited suffix
def Keccak(r, c, input, d, outputLen):
    # Initialization
    outputBytes = bytearray()
    rateInBytes = r//8 #integer division to set rate to bytes
    blockSize = 0
    inputOffset = 0
    S = bytearray([0 for i in range(200)]) # State initialization

    # Padding
    S[blockSize] = S[blockSize] ^ d
    if (((d & 0x80) != 0) and (blockSize == (rateInBytes-1))):
        S = KeccakF1600(S)
    S[rateInBytes-1] = S[rateInBytes-1] ^ 0x80
    # Absorbing Phase
    while(inputOffset < len(input)):
        blockSize = min(len(input)-inputOffset, rateInBytes)
        for i in range(blockSize):
            S[i] = S[i] ^ input[i+inputOffset]
        inputOffset = inputOffset + blockSize
        if (blockSize == rateInBytes):
            S = KeccakF1600(S)
            blockSize = 0
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
