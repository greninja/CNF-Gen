import numpy as np 
from z3 import *
import time

#Synthesizing the dataset
inputs = [np.random.randint(0,2,6) for _ in xrange(5)]
outputs = [np.random.randint(0,2,1) for _ in xrange(5)]
trueoutputs = [i for i, x in enumerate(outputs) if x==1]                                                    
falseoutputs = [i for i, x in enumerate(outputs) if x==0]
on_indices = map(lambda index : np.where(inputs[index] == 1)[0], xrange(len(inputs)))
off_indices = map(lambda index : np.where(inputs[index] == 0)[0], xrange(len(inputs)))

def get_models(F):
    """
    Return all the satisfying models of the clauses given in 'F'.
    This piece of code exists primarily because Z3Py does not have 
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

# Producing the contraint clauses for minterms at which the function evaluates to 1
ON_ON_MATRIX = []
for clause in range(1,3): 
    temp = []
    for index in trueoutputs:
        arr = []
        for elem in on_indices[index]:
            pi = Bool('p'+str(elem)+str(clause))
            arr.append(pi)
        temp.append(arr)
    ON_ON_MATRIX.append(temp)

OFF_OFF_MATRIX = []
for clause in range(1,3): 
    temp = []
    for index in trueoutputs:
        arr = []
        for elem in off_indices[index]:
            ni = Bool('n'+str(elem)+str(clause))
            arr.append(ni)
        temp.append(arr)
    OFF_OFF_MATRIX.append(temp)  

# Combining the clauses from the individual matrices
matrix = [] 
for i in xrange(len(ON_ON_MATRIX)):
    for j in xrange(len(ON_ON_MATRIX[0])):
        matrix.append(Or(ON_ON_MATRIX[i][j] + OFF_OFF_MATRIX[i][j]))

# Producing the contraint clauses for minterms at which the function evaluates to 0
ON_OFF_MATRIX = []
for clause in range(1, 3):          
    temp = []                              
    for index in falseoutputs:                                      
       arr = []
       for elem in on_indices[index]: 
           ni = Bool('n'+str(elem)+str(clause))
           arr.append(ni)
       temp.append(arr)
    ON_OFF_MATRIX.append(temp)

OFF_ON_MATRIX = []
for clause in range(1,3):           
    temp = []                              
    for index in falseoutputs:                                      
        arr = []
        for elem in off_indices[index]:
            pi = Bool('p'+str(elem)+str(clause))
            arr.append(pi)
        temp.append(arr)
    OFF_ON_MATRIX.append(temp)

for i in xrange(len(ON_OFF_MATRIX)):
    for j in xrange(len(ON_OFF_MATRIX[0])):
        matrix.append(Or(ON_OFF_MATRIX[i][j] + OFF_ON_MATRIX[i][j]))

#Generating all the satisfying assignments
start_time = time.time()
models = get_models(matrix)
end_time = time.time()

# Retrieving the values of variables from the models returned
vec = BoolVector('n', 10)
G = [Or(vec)]
models = get_models(G) 
for solution in models:
    length = len(solution)
    for j in range(length):
        print solution[solution[j]]
    print "\n"
# For variables that are not present in the satisfying models implying they could take either of the values,
# do not consider them in final solution because their values wont really matter