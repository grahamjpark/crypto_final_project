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



def serverFlip():

	HOST = ''   # Symbolic name meaning all available interfaces
	PORT = 12351 # Arbitrary non-privileged port
	 
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print 'Socket created'
	 
	#Bind socket to local host and port
	try:
	    s.bind((HOST, PORT))
	except socket.error as msg:
	    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	    sys.exit()
	     
	print 'Socket bind complete'
	 
	#Start listening on socket
	s.listen(10)
	print 'Socket now listening'


	#wait to accept a connection - blocking call
	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])

	#Flips the coin and sends the resulting hash to client    
	flipCoin()
	toSend = 'COINFLIP-PROCESS\nHASH\n' + getHash()
	conn.sendall(toSend)

	#Receiving from client
	data = conn.recv(1024)

	dataParts = data.split('\n')

	bitGuess = -1
	if 'COINFLIP-PROCESS' in dataParts[0] and 'BIT-GUESS' in dataParts[1]:
		bitGuess = int(dataParts[2])

	toSend = 'COINFLIP-PROCESS\nRANDOM-NUMBER\n' + str(getRandom())
	conn.sendall(toSend)

	print 'Bit from random number: ' + str(getBitFromRandom(getRandom()))
	challenge = -1
	if getBitFromRandom(getRandom()) == bitGuess:
		challenge = 1
	else:
		challenge = 0

	print 'Challenge: ' + str(challenge)


	while True:
	     
	    #Receiving from client
	    data = conn.recv(1024)
	    if not data: 
	        break
	 
	#came out of loop
	conn.close()

	s.close()

	return challenge





def checkHash(random):
    #Sets up the hash function
    m = hashlib.md5()
    #Adds the random hex string to be hashed
    m.update(random)
    #Hashes the string (which outputs stuff) and converts that to a hex string
    tempHash = binascii.hexlify(m.digest());
    return tempHash == getHash()

def clientFlip():
	s = socket.socket()         # Create a socket object
	host = socket.gethostname() # Get local machine name
	port = 12351                # Reserve a port for your service.

	s.connect((host, port))
	data = s.recv(1024)
	dataParts = data.split('\n')

	if 'COINFLIP-PROCESS' in dataParts[0] and 'HASH' in dataParts[1]:
	    setHash(dataParts[2])
	    print 'Recieved Hash'

	toSend = 'COINFLIP-PROCESS\nBIT-GUESS\n' + str(getCommitBit())
	s.sendall(toSend)
	print 'Sent Guess of: ' + str(getCommitBit())

	data = s.recv(1024)
	dataParts = data.split('\n')

	random = ""
	if 'COINFLIP-PROCESS' in dataParts[0] and 'RANDOM-NUMBER' in dataParts[1]:
	    random = dataParts[2]
	    if not checkHash(random):
	        print 'Wat, the hashes didn\'t match, pls'
	        exit()

	challenge = -1

	if getBitFromRandom(random) == getCommitBit():
	    challenge = 1
	else:
	    challenge = 0

	print 'Challenge: ' + str(challenge)

	s.close()                     # Close the socket when done
	return challenge