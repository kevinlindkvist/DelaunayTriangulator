DelaunayTriangulator
====================

An implementation of Steve Fortunes incremental Delaunay triangulation algorithm.

This program was written and tested using Python 2.7.3, which can be found at http://www.python.org/getit/releases/2.7.3/, but should work using later versions of Python as well. I didn’t use any special libraries, but I did stumble upon an imple- mentation of the basic incremental version of the algorithm in C + + (without the conflict list) by Dani Lischinski that can be found at http://www.karlchenofhell.org/cppswp/ lischinski.pdf. In many places I sacrificed elegance for performance, which in Python means a lot of inline code instead of method calls. The times in the below table are mea- sured without garbage collection (except for the 1,000,000 point set), this gives around a 10 second improvement for the 100,000 set. To see the timing data, use [-v]. I would also recommend at least 16GB of memory in order to run the largest point set, otherwise there will be thrashing, and it wont be pretty.

python delaunay.py [option] inputfile.node

-v: Will run the program in verbose mode, outputting progress etc. 

-c: Will run the program using a conflict list for point location 

-nele: Will not output .ele file

-edge: Will output .edge file

-p: Will profile using ttimeu100000.node

-nfs: Need for speed (no garbage collection)

-mp: Will output GC information

