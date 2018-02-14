import numpy as np
with open("input.txt","w+") as f:                                                 
  for _ in xrange(5):
     for _ in xrange(6):
         f.write(str(np.random.randint(0,2)))
     f.write(" ")
     f.write(str(np.random.randint(0,2)))
     f.write("\n")  