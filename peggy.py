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

def doneHere(soc):
	soc.close()                    # Close the socket when done
	exit()

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
		doneHere(soc)
	if 'False' in dataParts[1]:
		print 'Victor reported a failed test. Exiting.'
		doneHere(soc)

if '-help' in sys.argv[1]:
	print 'This file runs Peggy (as a client), who is the prover in our ZPK'
	print 'Args are as follow: G1 text file, G2 text file, B2 text file, and a port number Peggy and Victor should use'
	print 'For example:'
	print 'python peggy.py data/gone02.txt data/input02.txt data/beta02.txt 12370'
	doneHere(soc)

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

data = soc.recv(1024)
dataParts = data.split('\n')

if 'NUMBER-OF-TESTS' not in dataParts[0]:
	print 'Number of tests was not recieved'
	doneHere(soc)
NUM_TESTS = int(dataParts[1])

print 'Proving to Victor using ' + str(NUM_TESTS) + ' round(s)'
for i in range(NUM_TESTS):
	attemptZPK()
print 'All tests passed.'
doneHere(soc)


