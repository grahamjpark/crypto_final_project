import random
one = 0
zero = 0

for i in range(1000000):
	if random.sample(range(0,2), 1)[0] == 1:
		one += 1
	else:
		zero += 1
print 'One: ' + str(one)
print 'Zero: ' + str(zero)
