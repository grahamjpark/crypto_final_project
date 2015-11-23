#!/usr/bin/python

import random;
from getMatrix import *;

n = int(sys.argv[1]);
remove = random.randint(n / 4, 3 * n / 4);
gtwo = numpy.matrix(generateMatrix(n));
gone = numpy.matrix(gtwo);
index = -1;
for i in range(remove):
    index = (index + 1) % n;
    hasRemoved = gone[index, index] != -1;
    removeNode(gone, index);
'''
beta = [0 for i in range(n)];
for i in range(0, remove):
    beta[i] = (i + 1) % (remove);
for i in range(remove, n):
    beta[i] = i;
print beta;
'''

beta = generateIsomorphismDefinitionMatrix(n);
gprime = getIsomorphism(gone, beta);
print numpy.matrix(gone);
print '~'
print numpy.matrix(gprime);
print '~'

for i in range(n):
    for j in range(i, n):
        if gprime[i, j] == -1:
            gprime[i, j] = random.randint(0, 1);
            gprime[j, i] = gprime[i, j];             
gtwo = gprime;

print numpy.matrix(gtwo);

gone = matrixToString(gone);
gtwo = matrixToString(gtwo);
beta = matrixToString(beta);

outfile = open("data/gone%02d.txt" % n, "w");
outfile.write(gone);
outfile.close();
outfile = open("data/gtwo%02d.txt" % n, "w");
outfile.write(gtwo);
outfile.close();
outfile = open("data/beta%02d.txt" % n, "w");
outfile.write(beta);
outfile.close();

