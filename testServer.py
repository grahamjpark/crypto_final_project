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

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 12313 # Arbitrary non-privileged port
 
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
print 'I wait now'
data = conn.recv(1024)
print '|' + data + '|'

dataParts = data.split('\n')

bitGuess = -1
if 'COINFLIP-PROCESS' in dataParts[0] and 'BIT-GUESS' in dataParts[1]:
	bitGuess = int(dataParts[2])
	print str(bitGuess)

conn.sendall(str(getRandom()))

challenge = -1
if getBitFromRandom(getRandom()) == bitGuess:
	challenge = 1
else:
	challenge = 0

print 'challenge: ' + str(challenge)
conn.close()
 
s.close()