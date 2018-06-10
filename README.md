# Overview of this repo:


Hello, here I am generating 2-CNF boolean functions by encoding the search for them as a SAT problem. I am currently using Z3Py (Python Interface for Z3 Solver) for generating satisfying assingments.


## Quick Installation steps for Z3Py:

1. Head over to [Z3's github page](https://github.com/Z3Prover/z3) and download the zip file
2. unzip the folder in local machine
3. In the root directory of the folder, type 
	```
	python scripts/mk_make.py --prefix=*path to home directory* --python
	```
4. Now you could possibly face make exceptions/errors stating "C++ compiler not found" and "C compiler not found".    In such a situation you need to set the CXX and CC environment variable. You could do it by:

   - First locate where g++ and gcc is sitting in your machine:
   ```
   whereis g++
   ```
   and 
   ```
   whereis gcc
   ```
   - Select the 'usr' path and type (for g++ compiler):
   ```
   $~ CXX=/path/to/g++/compiler
   $~ export CXX
   ```

   for gcc compiler:
   ```
   $~ CC=/path/to/gcc/compiler
   $~ export CC
   ```

5. cd build
6. make
7. sudo make install
