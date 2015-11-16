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
    nodes = [[0 for i in range(rowCount)] for i in range(rowCount)];
    for i in range(rowCount):
        for j in range(rowCount):
            nodes[i][j] = int((rows[i].split(" "))[j]);
    return nodes;

def getIsomorphismDefinition(n):
    definition = list(range(n));
    random.shuffle(definition);
    return definition;

def getIsomorphismDefinitionMatrix(definition):
    n = len(definition);
    nodes = [[0 for i in range(n)] for i in range(n)];
    for i in range(n):
        nodes[i][definition[i]] = 1;
    return nodes;

def getIsomorphism(matrix, isomorphism):
    pi = numpy.matrix(isomorphism);
    pit = numpy.transpose(pi);
    m = numpy.matrix(matrix);
    return pi * m * pit;

def getMatrixTest():
    filename = sys.argv[1];
    matrix = getMatrixFromFile(filename);
    print matrix;

def getIsomorphismTest():
    n = 4;
    definition = getIsomorphismDefinition(n);
    pi = getIsomorphismDefinitionMatrix(definition);
    matrix = numpy.random.randint(2, size=(n, n));
    for i in range(n):
        matrix[i][i] = 0;
        for j in range(n):
            matrix[i][j] = matrix[j][i];
    isomorphism = getIsomorphism(matrix, pi);
    print matrix;
    print definition;
    print pi;
    print isomorphism;

print "Matrix tests";
getMatrixTest();
print "Isomorphism tests";
getIsomorphismTest();

