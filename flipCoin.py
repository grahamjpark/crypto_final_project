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
__bit = 0
__flipped = 0
__commitBit = -1

def flipCoin():
	#Uses OS to generate 124 bit random, then converts it to hexadecimal string
	rand = binascii.hexlify(os.urandom(124))
	# print '~~~~~~~Random Number~~~~~~~'
	# print rand
	global __rand
	__rand = rand

	# print '~~~~~~~Hash of Random~~~~~~~'
	#Sets up the hash function
	m = hashlib.md5();
	#Adds the random hex string to be hashed
	m.update(rand)
	#Hashes the string (which outputs stuff) and converts that to a hex string
	global __hash
	__hash = binascii.hexlify(m.digest());
	# print __hash

	# print '~~~~~~~First Char of Hash and Commitment~~~~~~~'
	#Selects the first char in that random hex string
	# print rand[0:1]
	#Converts that char to an int and takes it mod 2 to get the bit commitment
	__bit = ord(rand[0:1]) % 2
	# print __bit
	global __flipped
	flipped = 1
	print 'Coin fliped. Variables set'

def getRandom():
	if __flipped:
		return __rand
	else:
		return -1

def getHash():
	return __hash

def getBit():
	if __flipped:
		return __bit
	else:
		return -1

def setHash(hash):
	global __hash
	__hash = hash

def getCommitBit():
	global __commitBit
	if __commitBit == -1:
		__commitBit = random.sample(range(0,2), 1)[0] 

	return __commitBit

def getBitFromRandom(random):
	return ord(rand[0:1]) % 2