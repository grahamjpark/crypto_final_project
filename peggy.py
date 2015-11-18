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

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 12346 # Arbitrary non-privileged port

def flipCoin(connection):
	#Uses OS to generate 124 bit random, then converts it to hexadecimal string
	rand = binascii.hexlify(os.urandom(124))
	print '~~~~~~~Random Number~~~~~~~'
	print rand

	print '~~~~~~~Hash of Random~~~~~~~'
	#Sets up the hash function
	m = hashlib.md5();
	#Adds the random hex string to be hashed
	m.update(rand)
	#Hashes the string (which outputs stuff) and converts that to a hex string
	print binascii.hexlify(m.digest());


	print '~~~~~~~First Char of Hash and Commitment~~~~~~~'
	#Selects the first char in that random hex string
	print rand[0:1]
	#Converts that char to an int and takes it mod 2 to get the bit commitment
	print ord(rand[0:1]) % 2


 
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
 
#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #Sending message to connected client
    conn.send('Thank you for connecting. Bye.')
    #conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
     
    #infinite loop so that function do not terminate and thread do not end.
    while True:
         
        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        if not data: 
            break
     
        conn.sendall(reply)
     
    #came out of loop
    conn.close()
 
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    conn, addr = s.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
     
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    start_new_thread(clientthread ,(conn,))
 
s.close()
