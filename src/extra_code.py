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

pmatrix = []
for index in trueoutputs:
    parr = []
    for elem in on_indices[index]:
        pi = Bool('p'+str(elem))
        parr.append(pi)
    pmatrix.append(parr)

# For variables that are not present in the satisfying models implying they could take either of the values,
# do not consider them in final solution because their values wont really matter

"""
multiprocessing code

from multiprocessing import Process
p = Process(target=get_models, args=[clauses])
p.start()
"""

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