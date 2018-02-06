import numpy as np 
from z3 import *

#Creating synthesized dataset
inputs, outputs = [np.random.randint(0,2,6) for _ in xrange(5)], [np.random.randint(0,2,1) for _ in xrange(5)]
trueoutputs, falseoutputs = [i for i, x in enumerate(outputs) if x==1], \
                                                    [i for i, x in enumerate(outputs) if x==0]
on_indices = map(lambda index : np.where(inputs[index] == 1)[0], xrange(len(inputs)))
off_indices = map(lambda index : np.where(inputs[index] == 0)[0], xrange(len(inputs)))

pmatrix = []
for index in trueoutputs:
    parr = []
    for elem in on_indices[index]:
        pi = Bool('p'+str(elem))
        parr.append(pi)
    pmatrix.append(parr)

ndashmatrix = []
for index in trueoutputs:
    ndasharr = []
    for elem in on_indices[index]:
        ni = Bool('n`'+str(elem))
        ndasharr.append(ni)
    ndashmatrix.append(ndasharr)

# All-SAT procedure in Z3Py
x, y, z = Bools('x y z') 
# Return all the satisfying models of the clauses given in 'F' 
def get_models(F):
    result = []
    s = Solver()
    s.add(F)
    while s.check() == sat:
        m = s.model()
        result.append(m)
        # Create a new constraint the blocks the current model
        block = []
        for d in m:
            # d is a declaration
            if d.arity() > 0:
                raise Z3Exception("uninterpreted functions are not supported")
            # create a constant from declaration
            c = d()
            if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                raise Z3Exception("arrays and uninterpreted sorts are not supported")
            block.append(c != m[d])
        s.add(Or(block))
    return result

# 4.2.18 - Getting values of variables of a BoolVector
vec = BoolVector('n', 10)
G = [Or(vec)]
models = get_models(G, 22) # since it returns exactly 22 models
for solution in models:
    length = len(solution)
    for j in range(length):
        print solution[solution[j]]
    print "\n"