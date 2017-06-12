def ndice(n, seq=""):
    if n == 1:
        for i in range(1, 7):     
            print seq + str(i)
    else:
        for i in range(1, 7):
            ndice(n-1, seq + str(i))        

ndice(3) #prints all 216 combintions. 