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

#Generating all the satisfying assignments
start_time = time.time()    
models = get_models(clauses)
end_time = time.time()

# Retrieving the values of variables from the models returned
functions = []
for model in models:
    modlen = len(model)
    temp = []
    for j in range(modlen):
        if model[model[j]] == True:
            temp.append(model[j])
    functions.append(temp)

# For variables that are not present in the satisfying models implying they could take either of the values,
# do not consider them in final solution because their values wont really matter

"""
Piece of multiprocessing code

from multiprocessing import Process
p = Process(target=get_models, args=[matrix])
p.start()
"""

"""
Alternative method for generating sat models for '1' minterms 
('And'ing both the clauses for each minterm)
    
clauses = []
for index in trueoutputs:   
    main_array = []
    for clause in xrange(1,3):
        clause_array = []
        for elem in on_indices[index]:
            pi = Bool('p'+str(elem)+str(clause))
            clause_array.append(pi)
        for elem in off_indices[index]:
            ni = Bool('n'+str(elem)+str(clause))
            clause_array.append(ni)
        main_array.append(Or(clause_array)) 
    clauses.append(And(main_array))

for index in falseoutputs:
    main_array = []
    for clause in xrange(1, 3):
        clause_array = []
        for elem in on_indices[index]:
            ni = Bool('n'+str(elem)+str(clause))
            clause_array.append(ni)
        for elem in off_indices[index]:
            pi = Bool('p'+str(elem)+str(clause))
            clause_array.append(pi)
        main_array.append(Or(clause_array))
    clauses.append(And(main_array))
"""