#This stuff can be used to bit commitment.
#It out puts a random, finds the hash of that random, then figures out whether that means a 1 or a 0

import hashlib
import random
import sys
import os
import math
import binascii

#Uses OS to generate 124 bit random, then converts it to hexadecimal string
rand = binascii.hexlify(os.urandom(124))
print '~~~~~~~Random Number~~~~~~~'
print rand

print '~~~~~~~Hash of Random~~~~~~~'
#Sets up the hash function
m = hashlib.md5();
#Adds the random hex string to be hashed
m.update(rand)
#Hashes the string (which outputs stuff) and converts that to a hex string
print binascii.hexlify(m.digest());


print '~~~~~~~First Char of Hash and Commitment~~~~~~~'
#Selects the first char in that random hex string
print rand[0:1]
#Converts that char to an int and takes it mod 2 to get the bit commitment
print ord(rand[0:1]) % 2