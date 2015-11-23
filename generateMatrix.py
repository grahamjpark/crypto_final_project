#!/usr/bin/python

import random;
from getMatrix import *;

n = int(sys.argv[1]);
remove = random.randint(1, n - 1);
gtwo = generateMatrix(n);
gone = numpy.matrix(gtwo);
for i in range(remove):
   removeNode(gone, random.randint(0, n - 1));
gone = matrixToString(gone) + "\n";
gtwo = matrixToString(gtwo) + "\n";
beta = matrixToString(generateIsomorphismDefinitionMatrix(n)) + "\n";

outfile = open("data/gone%02d.txt" % n, "w");
outfile.write(gone);
outfile.close();
outfile = open("data/gtwo%02d.txt" % n, "w");
outfile.write(gtwo);
outfile.close();
outfile = open("data/beta%02d.txt" % n, "w");
outfile.write(beta);
outfile.close();

