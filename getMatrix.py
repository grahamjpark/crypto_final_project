#!/usr/bin/python

import sys;

#args: String filename
#return: 2d int array adjacency matrix
def getMatrix(filename):
    fd = open(filename, 'r');
    rows = fd.read().split("\n");
    fd.close();
    rowCount =  len(rows) - 1; #last element in rows is empty
    nodes = [[0 for i in range(rowCount)] for i in range(rowCount)];
    for i in range(rowCount):
        for j in range(rowCount):
            nodes[i][j] = int((rows[i].split(" "))[j]);
    return nodes;

def getMatrixTest():
    filename = sys.argv[1];
    matrix = getMatrix(filename);
    print matrix;
    print matrix[0][0] + matrix[0][1];

getMatrixTest();
