import numpy as np 
from z3 import *
import time
import pprint

#Synthesizing the dataset
inputs = [np.random.randint(0,2,6) for _ in xrange(5)]
outputs = [np.random.randint(0,2,1) for _ in xrange(5)]
trueoutputs = [i for i, x in enumerate(outputs) if x==1]                                                    
falseoutputs = [i for i, x in enumerate(outputs) if x==0]
on_indices = map(lambda index : np.where(inputs[index] == 1)[0], xrange(len(inputs)))
off_indices = map(lambda index : np.where(inputs[index] == 0)[0], xrange(len(inputs)))

def get_models(F):
    """
    Returns all the satisfying models of the clauses given in 'F'.
    This function exists primarily because Z3Py does not have 
    inbuilt support for returning all the satisfying models.
    Hence we explicitly put a constraint to not generate a model
    similar to previous ones.
    """
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

# Generating the clauses
clauses = []
for index in trueoutputs:   
    for clause in xrange(1,3):
        clause_array = []
        for elem in on_indices[index]:
            pi = Bool('p'+str(elem)+str(clause))
            clause_array.append(pi)
        for elem in off_indices[index]:
            ni = Bool('n'+str(elem)+str(clause))
            clause_array.append(ni)
        clauses.append(Or(clause_array))

for index in falseoutputs:
    for clause in xrange(1, 3):
        clause_array = []
        for elem in on_indices[index]:
            ni = Bool('n'+str(elem)+str(clause))
            clause_array.append(ni)
        for elem in off_indices[index]:
            pi = Bool('p'+str(elem)+str(clause))
            clause_array.append(pi)
        clauses.append(Or(clause_array))

# Additional clauses for restricting 2 polarities of the same variable to be not present 
# in the same clause
parray, narray = [], []
for i in xrange(len(inputs)+1):
    for j in xrange(1, 3):
        pi, ni = Not(Bool('p'+str(i)+str(j))), Not(Bool('n'+str(i)+str(j)))
        parray.append(pi); narray.append(ni)
zipped = zip(parray, narray)
for c in zipped:
    clauses.append(Or(c))

# Following piece of code creates:
# (1) additional constraints so that each clause in the function has atmost 2 'True' assignments
# (2) a dictionary for mapping encoding variables to function variables
dictionary = {}
for clause_indice in xrange(1, 3):
    array = []
    for var_indice in xrange(6):
        pi, ni = 'p'+str(var_indice)+str(clause_indice), 'n'+str(var_indice)+str(clause_indice)
        dictionary[pi], dictionary[ni] = 'x'+str(var_indice), 'Not(x'+str(var_indice)+')'
        array.append(Bool(pi)); array.append(Bool(ni))
    clauses.append(Sum([If(x, 1, 0) for x in array]) <= 2)

#Generating all the satisfying assignments
start_time = time.time()    
models = get_models(clauses)
end_time = time.time()
print "Time taken to generate the models : {} \n , \
        Number of models generated : {}".format((end_time - start_time), len(models))

# Constructing the possible functions (as of now : just 5 functions)
samples = models[:5]
functions = []
for sample in samples:
    c1, c2 = [], []
    for d in sample:
        if sample[d] == True:
            if str(d).endswith('1'):
                c1.append(dictionary[str(d)])
            else:
                c2.append(dictionary[str(d)])
    string = ''
    if len(c1) == 2:
        string += c1[0]+' or '+c1[1]+' AND '
    elif len(c1) == 1:
        string += c1[0] + ' AND '
    else:
        pass
        
    if len(c2) == 2:
        string += c2[0]+' or ' +c2[1]
    elif len(c2) == 1:
        string += c2[0]
    else:
        pass
    functions.append(string)

pprint.pprint(functions)

# For variables that are not present in the satisfying models implying they could take either of the values,
# do not consider them in final solution because their values wont really matter

"""
multiprocessing code

from multiprocessing import Process
p = Process(target=get_models, args=[clauses])
p.start()
"""