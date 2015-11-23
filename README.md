#Zero Knowledge Proof through Subgraph Isomorphism 
CS 355 Final Project

## Team Members
&nbsp;&nbsp;Abhijay Gupta<br />
&nbsp;&nbsp;Graham Park<br />
&nbsp;&nbsp;John Du<br />
&nbsp;&nbsp;Pranav Punjabi<br />

##Running the code
Follow the methods below to run the code, or run the file followed by '-help'
###Server
Generating failure
- python victor.py data/gone07.txt data/gtwo07.txt PORT NUM_TESTS

Generating success
- python victor.py data/gone05.txt data/gtwo05.txt PORT NUM_TESTS

    
###Client
Generating failure
- python peggy.py data/gone07.txt data/gtwo07.txt data/beta07.txt PORT NUM_TESTS

Generating success
- python peggy.py data/gone05.txt data/gtwo05.txt data/beta05.txt PORT NUM_TESTS

### Generate Random Matrices
Generates G1(gone), G2(gtwo) and beta with the specified number of nodes
- python generateMatrix.py NUM_NODES


##Grade

- [x] Sockets (20pts)
- [x] Commitment (20pts)
- [x] Random gen (5pts)
- [x] Multiple runs (5pts)
- [x] Different graph sizes (5pts)
- [x] Other things (45pts)

##Information

- [Project Slides](https://www.cs.purdue.edu/homes/jiang97/CS355Project_modified.pdf)
- [Homework (look at Q4)](https://www.cs.purdue.edu/homes/mja/hwks/hwk2.pdf)
- [Homework Solution](https://www.cs.purdue.edu/homes/mja/hwks/2sol.pdf)

##Dates
- Nov. 23: Submit to TA by email 
- Nov. 30-Dec. 11: All group members must be present for demo
     
