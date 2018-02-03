import numpy as np 
from z3 import *

#Creating synthesized data
inputs, outputs = [np.random.randint(0,2,6) for _ in xrange(5)], [np.random.randint(0,2,6) for _ in xrange(5)]
indices = [i for i, x in enumerate(outputs) if x==1]

# Sample example
x1, x2, x3 = Bools('x1 x2 x3')
g = Goal()
g.add(Or(And(x1, Not(x2), x3), And(x1, Not(x2), Not(x3)), And(Not(x1), x2, x3)))
sim = Tactic('ctx-solver-simplify')
print sim(g) # This would print the simplified boolean expression 

# Date: 2.2.18
a = []
n = len(inputs)
z = BoolVector('z', n)
solve(Or(z))

# If there are two expressions
solve(Or(Or(z), Or(m)))

# Much better practice of solving
x, y = Bools('x y')
s = Solver()
s.add(Or(x, y))
m = s.model()
# 'm'  contains the satisfying assignments of variables. 




# TODO 3rd Feb, 18
1) See how to store output of solve() - Done : storing output of 'get_models' in an arrays
2) Write a summary of other approaches
3) Write the boolean formula for all the minterms instead of just one





from z3 import *
x, y, z = Bools('x y z')
# Return the first "M" models of formula list of formulas F 
def get_models(F, M):
    result = []
    s = Solver()
    s.add(F)
    while len(result) < M and s.check() == sat:
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
F = [And(Or(x, y), Or(y, z))]
get_models(F, 10)
# Returns the following:
# [[z = False, y = True, x = False],
#  [y = True, x = True],
#  [z = True, y = False, x = True],
#  [z = True, y = True, x = False]]

