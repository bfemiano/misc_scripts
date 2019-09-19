def isPowerOf2(n):
	return n & (n-1) == 0


for i in range(0, 257):
	if(isPowerOf2(i)):
		print("%i" % i)
