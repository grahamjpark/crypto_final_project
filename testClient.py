#http://www.tutorialspoint.com/python/python_networking.htm
#!/usr/bin/python           # This is client.py file

import hashlib
import random
import sys
import os
import math
import binascii
import socket
import sys
from thread import *
from flipCoin import *

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12351                # Reserve a port for your service.

def checkHash(random):
	#Sets up the hash function
	m = hashlib.md5()
	#Adds the random hex string to be hashed
	m.update(random)
	#Hashes the string (which outputs stuff) and converts that to a hex string
	tempHash = binascii.hexlify(m.digest());
	return tempHash == getHash()


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
