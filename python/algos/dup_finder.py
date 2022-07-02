import random

def find_dup(l, start, end):
    n = (start + end) / 2
    cnt_left = 0
    cnt_right = 0
    cnt_n = 0
    for i in range(len(l)):
        if l[i] <= n: 
            cnt_left += 1 
            if l[i] == n:
                cnt_n += 1
        else:
            cnt_right += 1
    is_left = cnt_left > n 
    if cnt_n == 2:
        return n 
    elif is_left:
        return find_dup(l, 0, n-1)
    else:
        return find_dup(l, n+1, end)
        

errors = 0
for i in range(1000): # Randomly build 1000k tests
    l = []
    r = random.randint(2, 100) # Randomly choose the array size.
    for i in range(1, r): #Exclusive cutoff at r means with the random insertion we get an array of length r-1, where the values range from 0 to r-1. 
        l.append(i)
    extra = random.randint(1,r-1) #And now we insert the duplicate to get length 'r'.
    l.append(extra)
    try:
        found = find_dup(l, 0, len(l)-1)
        if found != extra:
            errors += 1
    except RuntimeError:
        errors += 1
print "num errors", errors