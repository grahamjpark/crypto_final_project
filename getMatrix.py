#!/usr/bin/python

import random;
import numpy;
import sys;

#args: String filename
#return: 2d int array adjacency matrix
def getMatrixFromFile(filename):
    fd = open(filename, 'r');
    rows = fd.read().split("\n");
    fd.close();
    rowCount =  len(rows) - 1; #last element in rows is empty
    matrix = [[0 for i in range(rowCount)] for i in range(rowCount)];
    for i in range(rowCount):
        for j in range(rowCount):
            matrix[i][j] = int((rows[i].split(" "))[j]);
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

def commit(matrix):
    return matrix;

def peggyRound(gone, gtwo, beta, coinflip):
    betaMatrix = numpy.matrix(beta);
    n = len(gone);
    alpha = generateIsomorphismDefinition(n);
    alphaMatrix = getIsomorphismDefinitionMatrix(alpha);
    q = getIsomorphism(gtwo, alphaMatrix);
    #send commit(q);
    pi = numpy.matrix(alphaMatrix) * numpy.matrix(betaMatrix);
    qprime = getIsomorphism(gone, pi);
    print "~alpha:";
    print alpha;
    print "~beta:";
    print beta;
    print "~pi:";
    print pi;
    print "~q:";
    print q;
    print "~qprime:";
    print qprime;
    if (coinflip == 0):
        return (alpha, q);
    return (pi, qprime);

def victorRound(gone, gtwo, isomorphism, matrix, commitment, coinflip):
    #check matrix is same as commit
    #commit(matrix) == commitment
    if (coinflip == 0):
        q = getIsomorphism(gtwo, isomorphism);
        return (numpy.q == numpy.matrix).all();
    #check matrix is part of q (commitment)
    qprime = getIsomorphism(gone, isomorphism);
    return (numpy.qprime == numpy.matrix).all();

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
    matrix = getMatrixFromFile(sys.argv[1]);
    submatrix = getMatrixFromFile(sys.argv[2]);
    betaMatrix = getMatrixFromFile(sys.argv[3]);
#    n = len(matrix);
#    beta = generateIsomorphismDefinition(n);
    print "Round 0";
    peggyRound(matrix, submatrix, betaMatrix, 0);
    print "Round 1";
    peggyRound(matrix, submatrix, betaMatrix, 1);

print "Matrix tests";
getMatrixTest();
print "Isomorphism tests";
getIsomorphismTest();
print "Round tests";
roundTest();

