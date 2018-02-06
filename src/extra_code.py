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