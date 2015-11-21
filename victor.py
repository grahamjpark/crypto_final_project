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

############################## SERVER STUFF ##############################
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
##########################################################################


#Read in from files
submatrix = getMatrixFromFile(sys.argv[1]);
matrix = getMatrixFromFile(sys.argv[2]);

############################## ROUND ONE ##############################
data = conn.recv(1024) #recv(hashed, randomones)
dataParts = data.split('&')
if 'ROUND-ONE' not in dataParts[0]:
	print 'THINGS ARE OUT OF ORDER OR DON\'T HAVE PROPER HEADERS I DONE GOOFED OH NO PANIC'
	exit()
hashed = stringToMatrix(dataParts[1])
randomones = stringToMatrix(dataParts[2])

############################## COIN FLIP ##############################
coinFlip = serverFlip(conn)

############################## ROUND TWO ##############################
data = conn.recv(1024) # if 0 recv(alpha, q), else recv(pi, qprime)
dataParts = data.split('&')

alpha = numpy.random.rand(0,0)
q = numpy.random.rand(0,0)
pi = numpy.random.rand(0,0)
qprime = numpy.random.rand(0,0)

if 'ROUND-TWO' not in dataParts[0]:
	print 'THINGS ARE OUT OF ORDER OR DON\'T HAVE PROPER HEADERS I DONE GOOFED OH NO PANIC'
	exit()

if coinFlip == 0:
	alpha = stringToMatrix(dataParts[1])
	q = stringToMatrix(dataParts[2])
else:
	pi = stringToMatrix(dataParts[1])
	qprime = stringToMatrix(dataParts[2])

############################## ROUND THREE ##############################
data = conn.recv(1024)  #recv(randomtwos)
dataParts = data.split('&')

if 'ROUND-THREE' not in dataParts[0]:
	print 'THINGS ARE OUT OF ORDER OR DON\'T HAVE PROPER HEADERS I DONE GOOFED OH NO PANIC'
	exit()

randomtwos = stringToMatrix(dataParts[1])

if coinFlip == 1:
	victorRound(submatrix, matrix, pi, qprime, hashed, randomones, randomtwos, coinflip);
else:
	victorRound(submatrix, matrix, alpha, q, hashed, randomones, randomtwos, coinflip);

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