import numpy as np 
from z3 import *
from datetime import datetime
import pprint

# Synthesizing the dataset
inputs, outputs = [], []
with open("input.txt", "r") as f:
    data = f.readlines() 
for s in data:                   
    e = s.strip().split(" ")                                                                                                                
    arr = [] 
    for i in e[0]:                                                                                                                          
      arr.append(int(i))
    inputs.append(arr)
    outputs.append(int(e[1])) 
trueoutputs = [i for i, x in enumerate(outputs) if x==1]                                                    
falseoutputs = [i for i, x in enumerate(outputs) if x==0]
on_indices = map(lambda index : np.where(np.array(inputs[index]) == 1)[0], \
                                                             xrange(len(inputs)))
off_indices = map(lambda index : np.where(np.array(inputs[index]) == 0)[0], \
                                                             xrange(len(inputs)))

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

# Generating the constraint clauses
# Constraint 1:
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

# Constraint 2:
# Either of the CNF can be zero for the overall value to evaluate to zero
z1, z2 = Bools('z1 z2')
d = dict()
for clause_indice in xrange(1, 3):
    d['z'+str(clause_indice)] = Bool('z'+str(clause_indice))
clauses.append(Or(Not(z1), Not(z2))) 

# Constraint 3:
for index in falseoutputs:
    for clause in xrange(1,3):
        arr1, arr2 = [], []
        for elem in on_indices[index]:
            pi, ni = Bool('p'+str(elem)+str(clause)), Bool('n'+str(elem)+str(clause))
            arr1.append(ni); arr2.append(pi)
        for elem in off_indices[index]:
            pi, ni = Bool('p'+str(elem)+str(clause)), Bool('n'+str(elem)+str(clause))
            arr1.append(pi)
            arr2.append(ni)
        clauses.append(Or(And(Not(d['z'+str(clause)]), \
                                Or(arr1)), And(d['z'+str(clause)], Or(arr2))))

# Constraint 4:
# Additional constraints for restricting 2 polarities of the same variable  
# to be not present in the same clause
parray, narray = [], []
for i in xrange(len(inputs)+1):
    for j in xrange(1, 3):
        pi, ni = Not(Bool('p'+str(i)+str(j))), Not(Bool('n'+str(i)+str(j)))
        parray.append(pi); narray.append(ni)
zipped = zip(parray, narray)
for c in zipped:
    clauses.append(Or(c))

# Constraint 5:
# Following piece of code creates:
# (1) additional constraints so that each clause in the function has atmost
#     two 'True' assignments
# (2) a dictionary for mapping encoding variables to function variables
dictionary = dict()
for clause_indice in xrange(1, 3):
    clause_array = []
    for var_indice in xrange(6):
        pi, ni = 'p'+str(var_indice)+str(clause_indice), \
                                    'n'+str(var_indice)+str(clause_indice)
        dictionary[pi], dictionary[ni] = 'x'+str(var_indice), \
                                                'Not(x'+str(var_indice)+')'
        clause_array.append(Bool(pi)) 
        clause_array.append(Bool(ni))
    clauses.append(Sum([If(x, 1, 0) for x in clause_array]) <= 2)

# Generating all the satisfying assignments to the constraint clauses
start_time = datetime.now()   
models = get_models(clauses)
end_time = datetime.now()
total_time = (end_time - start_time).total_seconds()
print "Time taken to generate the models : {} \n  \
        Number of models generated : {}".format(total_time, len(models))

# Constructing the possible functions (as of now : just 5 random functions)
samples, functions = [], []
for rand in np.random.choice(len(models), 5, replace=False):
    samples.append(models[rand])
for sample in samples:
    c1, c2 = [], []
    for e in sample:
        if sample[e] == True and not str(e).startswith('z'):
            if str(e).endswith('1'):
                c1.append(dictionary[str(e)])
            else:
                c2.append(dictionary[str(e)])   
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