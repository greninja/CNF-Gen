import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("samplesize", type=int,
	   help="Number of input samples")
parser.add_argument("bitveclen", type=int,
	   help="Length of the input bit vectors")

args = parser.parse_args()
with open("input.txt","w+") as f:                                                 
  for _ in xrange(args.samplesize):
    for _ in xrange(args.bitveclen):
        f.write(str(np.random.randint(0,2)))
    f.write(" ")
    f.write(str(np.random.randint(0,2)))
    f.write("\n")  