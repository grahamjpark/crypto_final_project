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
from getMatrix import *
from matrixOperations import *

def attemptZPK():
	############################## ROUND ONE ##############################
	alpha, q, pi, qprime, randomones, randomtwos, hashed = peggyRoundOne(submatrix, matrix, betaMatrix);
	toSend = 'ROUND-ONE$' + matrixToString(hashed) + '$' + matrixToString(randomones)
	soc.send(toSend) # send(hashed, randomones) #this is the commitment

	############################## COIN FLIP ##############################
	coinflip = clientFlip(soc)

	############################## ROUND TWO ##############################
	toSend = 'ROUND-TWO$'
	if coinflip == 0:
	    toSend += matrixToString(alpha) + '$'
	    toSend += matrixToString(q)
	else:
	    toSend += matrixToString(pi) + '$'
	    toSend += matrixToString(qprime)
	soc.send(toSend)

	############################## ROUND THREE ##############################
	toSend = 'ROUND-THREE$' + matrixToString(randomtwos)
	soc.send(toSend)

	############################## CHECK RESULT ##############################
	data = soc.recv(1024)
	dataParts = data.split('\n')

	if 'RESULT' not in dataParts[0]:
		print 'THINGS ARE OUT OF ORDER OR DON\'T HAVE PROPER HEADERS I DONE GOOFED OH NO PANIC'
		print 'Had: ' + dataParts[0]
		print 'Expected: RESULT'
		exit()
	if 'False' in dataParts[1]:
		print 'Failed a test, aborting'
		exit()
	print 'DONE!!'


############################## SERVER STUFF ##############################
soc = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = int(sys.argv[4])                # Reserve a port for your service.

soc.connect((host, port))
##########################################################################

#Read in from files
submatrix = getMatrixFromFile(sys.argv[1]);
matrix = getMatrixFromFile(sys.argv[2]);
betaMatrix = getMatrixFromFile(sys.argv[3]);

for i in range(10):
	print 'TRYING'
	attemptZPK()

soc.close()                    # Close the socket when done
