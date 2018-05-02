# Final Project for CS490 Cryptography. 
## Python implementation of NIST Hash Function Competition finalists.

### NIST Hash Function Competition Evaluation
The NIST organization announced the Hash Function Competition in 2007, and a
winner was announced in 2012 which was Keccak. This was for SHA-3 (Secure Hash
Algorithm 3) because both SHA-1 and SHA-2 were cracked in some manner.
For our final project we will implement the five finalists in the competition: Blake,
Skein, Keccak, Grøstl, and JH. Our goal for this project is to better understand hashing
algorithms and how they work, as well as understanding what make Keccak the best
option for mainstream use. To do this we will use the NIST test vectors for our
implementations of the hash functions as well as the resources linked below. The NIST
test vectors we will use should be similar if not the same used to help determine the
winner of the hash function competition. The NIST test vectors include a large number
of test inputs, and the expected outputs for each test case. There is also a vector for bit
and byte oriented output.

the implementation of Grostl and BLAKE are the open source versions that can be found based
in the info in the file itself for that algorithm. JH and Skein not implemented so we used 
the data available from NIST and others to draw conclusions about them.

### Makefile Included

### Hash Functions
[BLAKE](https://en.wikipedia.org/wiki/BLAKE_(hash_function)), 
[Skein](http://www.skein-hash.info/about), 
[Keccak](https://keccak.team/keccak.html), 
[Grøstl](http://www.groestl.info/index.html), 
[JH](http://www3.ntu.edu.sg/home/wuhj/research/jh/index.html)

### Other links
[List of Finalists](https://en.wikipedia.org/wiki/NIST_hash_function_competition#Finalists)

[NIST hash function test page](https://csrc.nist.gov/Projects/Cryptographic-Algorithm-Validation-Program/Secure-Hashing)

[NIST hash function testing documentation (SHA-3)](https://csrc.nist.gov/CSRC/media/Projects/Cryptographic-Algorithm-Validation-Program/documents/sha3/sha3vs.pdf)

[NIST hash function test cases downloads](https://csrc.nist.gov/Projects/Cryptographic-Algorithm-Validation-Program/Secure-Hashing)

[NIST final report](https://nvlpubs.nist.gov/nistpubs/ir/2012/NIST.IR.7896.pdf)

## Constributors:
Mitchell Dzurisin
Matt Blough