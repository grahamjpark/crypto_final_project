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
	requestParts = recieved.split('\n')

	if 'COINFLIP-PROCESS' in requestParts[0]:
		if 'HASH' in requestParts[1]:
			setHash(requestParts[2])
			commitBit = random.sample(range(0,2), 1)[0] 
			conn.send("COINFLIP-PROCESS\nCOMMITMENT\n" + str(commitBit))
		
















	else if 'Random Number: ' in recieved:
		if not recvHash:
			#ERROR
			print "Error: Number was recieved but hash is null"
		else:
			recvNum = [15, recieved.__len__()]
			checkHash()




print s.recv(1024)
s.close                     # Close the socket when done