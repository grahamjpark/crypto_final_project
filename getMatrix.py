#!/usr/bin/python

import random;
import numpy;
import sys;
import hashlib;
import binascii;
import random;
import os;
from matrixOperations import *

def parseMatrix(string):
    rows = string.split("\n");
    rowCount = len(rows) - 1;
    matrix = [["" for i in range(rowCount)] for i in range(rowCount)];
    for i in range(rowCount):
        elements = rows[i].split(" ");
        for j in range(rowCount):
            matrix[i][j] = (elements[j]);
    return matrix;

def parseIntMatrix(string):
    matrix = parseMatrix(string);
    n = len(matrix);
    for i in range(n):
        for j in range(n):
            matrix[i][j] = int(matrix[i][j]);
    return matrix;

def matrixToString(matrix):
    return nmatrixToString(numpy.matrix(matrix));

def nmatrixToString(nmatrix):
    string = "";
    n = len(nmatrix);
    for i in range(n):
        for j in range(n):
            string += str(nmatrix[i, j]);
            if j < n - 1:
                string += " ";
        if i < n - 1:
            string += "\n";
    return string;

#args: String filename
#return: 2d int array adjacency matrix
def getMatrixFromFile(filename):
    fd = open(filename, 'r');
    matrix = parseIntMatrix(fd.read());
    fd.close();
    return matrix;

#args: n size of random adjacency matrix
#return: random adjacency matrix
def generateMatrix(n):
    matrix = numpy.random.randint(2, size=(n, n));
    for i in range(n):
        matrix[i][i] = 0;
        for j in range(n):
            matrix[i][j] = matrix[j][i];
    return matrix;    
    
#args: n size of random isomorphism definition
#return: array that represents the isomorphism such that [2, 1, 0] means node 0 now maps to 2
def generateIsomorphismDefinition(n):
    definition = list(range(n));
    random.shuffle(definition);
    return definition;

def generateIsomorphismDefinitionMatrix(n):
    return getIsomorphismDefinitionMatrix(generateIsomorphismDefinition(n));

#args: array that represents the isomorphism such that [2, 1, 0] means node 0 now maps to 2
#return: matrix form of the isomorphism
def getIsomorphismDefinitionMatrix(isomorphism):
    n = len(isomorphism);
    matrix = [[0 for i in range(n)] for i in range(n)];
    for i in range(n):
        matrix[i][isomorphism[i]] = 1;
    return matrix;

#args: matrix to change, isomorphism definition matrix
#return: an isomorph of matrix
def getIsomorphism(matrix, isomorphism):
    pi = numpy.matrix(isomorphism);
    pit = numpy.transpose(pi);
    m = numpy.matrix(matrix);
    return pi * m * pit;

#args: matrix to change, index to remove
#return: matrix with node removed represented as -1
def removeNode(matrix, index):
    n = len(matrix);
    for i in range(n):
        matrix[i,index] = -1;
        matrix[index,i] = -1;
    return matrix;

def generateRandoms():
    rand1 = binascii.hexlify(os.urandom(16));
    rand2 = binascii.hexlify(os.urandom(16));
    return (rand1, rand2);

def commit(matrix):
    n = len(matrix);
    randomones = [["" for i in range(n)] for i in range(n)];
    randomtwos = [["" for i in range(n)] for i in range(n)];
    hashed = [["" for i in range(n)] for i in range(n)];
    for i in range(n):
        for j in range(n):
            rand1, rand2 = generateRandoms();
            randomones[i][j] = rand1;
            randomtwos[i][j] = rand2;
            hashed[i][j] = hashelement(rand1 + rand2 + str(matrix[i, j]));
    return hashed, randomones, randomtwos;

def hashelement(string):
    m = hashlib.md5();
    m.update(string);
    hashstring = binascii.hexlify(m.digest());
    return hashstring;

def peggyRoundOne(gone, gtwo, beta):
    betaMatrix = numpy.matrix(beta);
    n = len(gone);
    alpha = generateIsomorphismDefinition(n);
    alphaMatrix = getIsomorphismDefinitionMatrix(alpha);
    q = getIsomorphism(gtwo, alphaMatrix);
    hashed, randomones, randomtwos = commit(q);
    pi = numpy.matrix(alphaMatrix) * numpy.matrix(betaMatrix);
    qprime = getIsomorphism(gone, pi);
    return (alphaMatrix, q, pi, qprime, randomones, randomtwos, hashed);

def peggyRoundTwo(alpha, q, pi, qprime, coinflip):
    if (coinflip == 0):
        print alpha;
        print q;
        #TODO: send(alpha, q);
    else:
        print pi;
        print qprime;
        #TODO: send(pi, qprime);

def peggyRoundThree(randomones, randomtwos):
    print "Peggy send final"
    #TODO: send(randomones, randomtwos);#send when victor asks for verify

def victorRound(gone, gtwo, isomorphism, matrix, hashed, randomones, randomtwos, coinflip):
    n = len(gtwo);
    #check matrix is part of q from commitment
    #check qprime is subgraph of q from commitment
    for i in range(n):
        for j in range(n):
            if (matrix[i, j] == -1):
                continue;
            check = hashelement(randomones[i][j] + randomtwos[i][j] + str(matrix[i, j]));
            if (hashed[i][j] != check):
                return False;

    if (coinflip == 0):
        #check q is the right isomorph
        q = getIsomorphism(gtwo, isomorphism);
        for i in range(n):
            for j in range(n):
                if (q[i, j] != matrix[i, j]):
                    return False;
    else:
        #check qprime is the right isomorph
        qprime = getIsomorphism(gone, isomorphism);
        for i in range(n):
            for j in range(n):
                if (qprime[i, j] != matrix[i, j]):
                    return False;
    return True;

#tests matrix file reading
def getMatrixTest():
    filename = sys.argv[1];
    matrix = getMatrixFromFile(filename);
    print matrix;

#tests isomorphism stuff
def getIsomorphismTest():
    n = 4;
    definition = generateIsomorphismDefinition(n);
    pi = getIsomorphismDefinitionMatrix(definition);
    matrix = generateMatrix(n);
    isomorphism = getIsomorphism(matrix, pi);
    print matrix;
    print definition;
    print pi;
    print isomorphism;
    print "Remove node 1";
    removeNode(matrix, 1);
    removeNode(isomorphism, definition[1]);
    print matrix;
    print isomorphism;

def roundTest():
    submatrix = getMatrixFromFile(sys.argv[1]);
    matrix = getMatrixFromFile(sys.argv[2]);
    betaMatrix = getMatrixFromFile(sys.argv[3]);
    print "Coinflip 0";
    coinflip = 0;
    alpha, q, pi, qprime, randomones, randomtwos, hashed = peggyRoundOne(submatrix, matrix, betaMatrix);
    peggyRoundTwo(alpha, q, pi, qprime, coinflip);
    peggyRoundThree(randomones, randomtwos);
    print victorRound(submatrix, matrix, alpha, q, hashed, randomones, randomtwos, coinflip);
    print "Coinflip 1";
    coinflip = 1;
    alpha, q, pi, qprime, randomones, randomtwos, hashed = peggyRoundOne(submatrix, matrix, betaMatrix);
    peggyRoundTwo(alpha, q, pi, qprime, coinflip);
    peggyRoundThree(randomones, randomtwos);
    print victorRound(submatrix, matrix, pi, qprime, hashed, randomones, randomtwos, coinflip);
    print matrix;
    print nmatrixToString(numpy.matrix(matrix));
    print matrixToString(matrix);
    print matrixToString(numpy.matrix(matrix));

# print "Matrix tests";
# getMatrixTest();
# print "Isomorphism tests";
# getIsomorphismTest();
# print "Round tests";
#roundTest();

