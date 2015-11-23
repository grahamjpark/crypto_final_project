#This stuff can be used to bit commitment.
#It out puts a random, finds the hash of that random, then figures out whether that means a 1 or a 0

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

def doneHere(conn):
	############################## SERVER STUFF ##############################
	# Waits for client to close first
	while True:
	     
	    #Receiving from client
	    data = conn.recv(1024)
	    if not data: 
	        break
	 
	#came out of loop
	conn.close()
	s.close()
	exit()

def attemptZPK():
	############################## ROUND ONE ##############################
	data = conn.recv(4096) #recv(hashed, randomones)
	dataParts = data.split('$')
	if 'ROUND-ONE' not in dataParts[0]:
		print 'THINGS ARE OUT OF ORDER OR DON\'T HAVE PROPER HEADERS I DONE GOOFED OH NO PANIC'
		doneHere(conn)
	hashed = parseMatrix(dataParts[1])
	randomones = parseMatrix(dataParts[2])

	############################## COIN FLIP ##############################
	coinFlip = serverFlip(conn)

	############################## ROUND TWO ##############################
	data = conn.recv(4096) # if 0 recv(alpha, q), else recv(pi, qprime)
	dataParts = data.split('$')

	alpha = numpy.random.rand(0,0)
	q = numpy.random.rand(0,0)
	pi = numpy.random.rand(0,0)
	qprime = numpy.random.rand(0,0)

	if 'ROUND-TWO' not in dataParts[0]:
		print 'THINGS ARE OUT OF ORDER OR DON\'T HAVE PROPER HEADERS I DONE GOOFED OH NO PANIC'
		doneHere(conn)

	if coinFlip == 0:
		alpha = parseIntMatrix(dataParts[1])
		q = numpy.matrix(parseIntMatrix(dataParts[2]))
	else:
		pi = parseIntMatrix(dataParts[1])
		qprime = numpy.matrix(parseIntMatrix(dataParts[2]))

	############################## ROUND THREE ##############################
	data = conn.recv(4096)  #recv(randomtwos)
	dataParts = data.split('$')

	if 'ROUND-THREE' not in dataParts[0]:
		print 'THINGS ARE OUT OF ORDER OR DON\'T HAVE PROPER HEADERS I DONE GOOFED OH NO PANIC'
		doneHere(conn)

	randomtwos = parseMatrix(dataParts[1])

	result = False

	if coinFlip == 1:
		result = victorRound(submatrix, matrix, pi, qprime, hashed, randomones, randomtwos, coinFlip);
	else:
		result = victorRound(submatrix, matrix, alpha, q, hashed, randomones, randomtwos, coinFlip);

	#if you want to see what happens when it's false
	# result = False; 

	toSend = 'RESULT\n' + str(result)
	conn.send(toSend)
	if not result:
		print 'Peggy failed a test, reported failure to Peggy and exiting'
		doneHere(conn)

if '-help' in sys.argv[1]:
	print 'This file runs Victor (as a server), who is the Verifier in our ZPK'
	print 'Args are as follow: G1 text file, G2 text file, a port number Peggy and Victor should use, and number of rounds'
	print 'For example:'
	print 'python victor.py data/gone02.txt data/input02.txt 12370 100'
	doneHere(conn)

############################## SERVER STUFF ##############################
HOST = ''   # Symbolic name meaning all available interfaces
PORT = int(sys.argv[3]) # Arbitrary non-privileged port
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
##########################################################################

#Read in from files
submatrix = getMatrixFromFile(sys.argv[1]);
matrix = getMatrixFromFile(sys.argv[2]);
NUM_TESTS = int(sys.argv[4])
toSend = 'NUMBER-OF-TESTS\n' + str(NUM_TESTS)
conn.send(toSend)

print 'Making Peggy prove using ' + str(NUM_TESTS) + ' round(s)'
for i in range(NUM_TESTS):
	attemptZPK()
print 'All tests passed.'
doneHere(conn)