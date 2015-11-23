# #!/usr/bin/python

# import random;
# import numpy;
# import sys;
# import hashlib;
# import binascii;
# import random;
# import os;


# #testing matrix
# #m = numpy.random.rand(3,2)
# randomones = [["" for i in range(4)] for i in range(4)];
# for i in range(4):
# 	for j in range(4):
# 		rand1 = binascii.hexlify(os.urandom(4));
# 		randomones[i][j] = rand1;


# def stringToMatrix(string):
# 	matrix = numpy.matrix(string)
# 	return matrix


# def matrixToString(matrix):
# 	arr = numpy.array(matrix)	
# 	return str(arr)



# # arr = matrixToString(randomones);
# # print arr
# matrix = stringToMatrix(randomones)
# print matrix
# string = matrixToString(matrix)
# print string

def test():
    # arr = matrixToString(randomones);
    # print arr
    matrix = stringToMatrix(randomones)
    print matrix
    string = matrixToString(matrix)
    print string

#test();

