#!/usr/bin/python

import random;
import numpy;
import sys;
import hashlib;
import binascii;
import random;
import os;


#testing matrix
m = numpy.random.rand(3,2)

def stringToMatrix(string):
	matrix = numpy.matrix(string)
	return matrix


def matrixToString(matrix):
	arr = numpy.array(m)	
	return arr


arr = matrixToString(m);
#print arr
matrix = stringToMatrix(arr)
#print matrix
