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
    conn.recv(2)
    size = int(conn.recv(16))
    data = ''
    while size > len(data):
        recvd = conn.recv(1024)
        if not recvd: 
            break
        data += recvd
    conn.sendall('ok')
    dataParts = data.split('$')
    if 'ROUND-ONE' not in dataParts[0]:
        print 'THINGS ARE OUT OF ORDER OR DON\'T HAVE PROPER HEADERS I DONE GOOFED OH NO PANIC'
        print 'Had: ' + dataParts[0]
        print 'Expected: ROUND-ONE'
        exit()
    hashed = parseMatrix(dataParts[1])
    randomones = parseMatrix(dataParts[2])

    ############################## COIN FLIP ##############################
    coinFlip = serverFlip(conn)

    ############################## ROUND TWO ##############################
    # if 0 recv(alpha, q), else recv(pi, qprime)
    conn.recv(2)
    size = int(conn.recv(16))
    data = ''
    while size > len(data):
        recvd = conn.recv(1024)
        if not recvd: 
            break
        data += recvd
    conn.sendall('ok')

    dataParts = data.split('$')

    alpha = numpy.random.rand(0,0)
    q = numpy.random.rand(0,0)
    pi = numpy.random.rand(0,0)
    qprime = numpy.random.rand(0,0)

    if 'ROUND-TWO' not in dataParts[0]:
        print 'THINGS ARE OUT OF ORDER OR DON\'T HAVE PROPER HEADERS I DONE GOOFED OH NO PANIC'
        print 'Had: ' + dataParts[0]
        print 'Expected: ROUND-TWO'
        exit()

    if coinFlip == 0:
        alpha = parseIntMatrix(dataParts[1])
        q = numpy.matrix(parseIntMatrix(dataParts[2]))
    else:
        pi = parseIntMatrix(dataParts[1])
        qprime = numpy.matrix(parseIntMatrix(dataParts[2]))

    ############################## ROUND THREE #############################
    #recv(randomtwos)
    conn.recv(2)
    size = int(conn.recv(16))
    data = ''
    while size > len(data):
        recvd = conn.recv(1024)
        if not recvd: 
            break
        data += recvd
    conn.sendall('ok')
    dataParts = data.split('$')

    if 'ROUND-THREE' not in dataParts[0]:
        print 'THINGS ARE OUT OF ORDER OR DON\'T HAVE PROPER HEADERS I DONE GOOFED OH NO PANIC'
        print 'Had: ' + dataParts[0]
        print 'Expected: ROUND-THREE'
        exit()

    randomtwos = parseMatrix(dataParts[1])

    result = False

    if coinFlip == 1:
        result = victorRound(submatrix, matrix, pi, qprime, hashed, randomones, randomtwos, coinFlip);
    else:
        result = victorRound(submatrix, matrix, alpha, q, hashed, randomones, randomtwos, coinFlip);

    #if you want to see what happens when it's false
    # result = False; 

    toSend = 'RESULT\n' + str(result)
    conn.sendall(toSend)
    if not result:
        print 'Peggy failed a test, reported failure to Peggy and exiting'
        doneHere(conn)

if '-help' in sys.argv[1]:
    print 'This file runs Victor (as a server), who is the Verifier in our ZPK'
    print 'Args are as follow: G1 text file, G2 text file, a port number Peggy and Victor should use, and number of rounds'
    print 'For example:'
    print 'python victor.py data/gone100.txt data/gtwo100.txt 12370 100'
    exit()

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
READ_SIZE = len(matrix) * len(matrix) * 112 + 10000*50
NUM_TESTS = int(sys.argv[4])
toSend = 'NUMBER-OF-TESTS\n' + str(NUM_TESTS)
conn.sendall(toSend)

print 'Making Peggy prove using ' + str(NUM_TESTS) + ' round(s)'
for i in range(NUM_TESTS):
    print 'Trying round'
    attemptZPK()
print 'All tests passed.'
doneHere(conn)