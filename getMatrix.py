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

print "Matrix tests";
getMatrixTest();
print "Isomorphism tests";
getIsomorphismTest();

