import numpy as np 

#Creating synthesized data
inputs, outputs = [np.random.randint(0,2,6) for _ in xrange(5)], [np.random.randint(0,2,6) for _ in xrange(5)]
indices = [i for i, x in enumerate(outputs) if x==1]
string = ""
for i in indices:
	l = inputs[i]
	for index in xrange(len(l)):
		if l[index]==1:
			string += "x"+str(index+1)+" AND "
		else:
			string += "NOT x"+str(index+1)+" AND "
	string += "    OR   "
print string