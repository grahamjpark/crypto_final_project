import socket               # Import socket module
import string
import random
from flipCoin import *


def checkHash():
	#Sets up the hash function
	m = hashlib.md5()
	#Adds the random hex string to be hashed
	m.update(recvNum)
	#Hashes the string (which outputs stuff) and converts that to a hex string
	tempHash = binascii.hexlify(m.digest());
	return tempHash == recvHash



conn = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12346                # Reserve a port for your service.

conn.connect((host, port))
recieved = conn.recv(1024)


while recieved:
	# The request will be broken up by new lines
	requestParts = recieved.split('\n')

	# Each newline will be more specific to which part of the program it is
	if 'COINFLIP-PROCESS' in requestParts[0]:
		if 'HASH' in requestParts[1]:
			# If its a hash that's been sent, calls setHash from flipCoin.py
			setHash(requestParts[2])

			# Picks a guess at whether it's odd or even and sends it
			commitBit = getCommitBit()
			conn.send("COINFLIP-PROCESS\nCOMMITMENT\n" + str(commitBit))
		if 'RANDOM-NUMBER' in requestParts[1]:
			bit = getBitFromRandom(requestParts[2])
			result = bit == getCommitBit() #This conditional might now work
print s.recv(1024)
s.close                     # Close the socket when done