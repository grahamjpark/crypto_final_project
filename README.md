#Zero Knowledge Proof through Subgraph Isomorphism 
CS 355 Final Project

## Team Members
&nbsp;&nbsp;Abhijay Gupta<br />
&nbsp;&nbsp;Graham Park<br />
&nbsp;&nbsp;John Du<br />
&nbsp;&nbsp;Pranav Punjabi<br />

##Things to Get Done
- [x] Set up python stuff
- [x] Set up sockets
- [x] Set up hash functions
- [x] Try to make da best random numbers
- [x] Set up bit commitment (communication between two programs)

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
- 

##Running the code

  Server<br />
    Generating failure<br />
     - python victor.py data/gone07.txt data/gtwo07.txt PORT NUM_TESTS <br />
    Generating success<br />
     - python victor.py data/gone05.txt data/gtwo05.txt PORT NUM_TESTS

    
  Client<br />
    Generating failure<br />
     - python peggy.py data/gone07.txt data/gtwo07.txt data/beta07.txt PORT NUM_TESTS<br />
    Generating success<br />
     - python peggy.py data/gone05.txt data/gtwo05.txt data/beta05.txt PORT NUM_TESTS
     
