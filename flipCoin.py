import hashlib
import random
import sys
import os
import math
import binascii
import socket
import sys
from thread import *

__rand = ""
__hash = ""
__flipped = 0
__commitBit = -1

#Called by Victor only
def flipCoin():
	#Uses OS to generate 124 bit random, then converts it to hexadecimal string
	rand = binascii.hexlify(os.urandom(256))
	global __rand
	__rand = rand

	#Sets up the hash function
	m = hashlib.md5();
	#Adds the random hex string to be hashed
	m.update(rand)
	#Hashes the string (which outputs stuff) and converts that to a hex string
	global __hash
	__hash = binascii.hexlify(m.digest());

	#Selects the first char in that random hex string
	#Converts that char to an int and takes it mod 2 to get the bit commitment
	__bit = getBitFromRandom(rand)
	global __flipped
	__flipped = 1
	print 'Coin fliped. Variables set'

def getRandom():
	if __flipped:
		return __rand
	else:
		return -1

#Called by peggy when hash is recieved
def setHash(hash):
	global __hash
	__hash = hash

def getHash():
	return __hash

#Called by peggy when they need to guess 0 or 1
def getCommitBit():
	global __commitBit
	if __commitBit == -1:
		__commitBit = random.sample(range(0,2), 1)[0] 
	return __commitBit

#To be called with getRandom to determine if number is odd or even
def getBitFromRandom(random):
	return ord(random[0:1]) % 2