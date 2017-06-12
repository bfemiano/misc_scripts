import sys
import itertools

def get_pascal(col, row):
    if row == 0:
        return [1]
    elif row == 1:
        return [1, 1]
    else:
        lower = get_pascal(col, row-1)
        return [1] + [lower[i] + lower[i+1] for i in range(len(lower) - 1)] + [1]

def pascal(col, row):
    return get_pascal(col, row)[col]

print pascal(0,2) #1
print pascal(1,2) #2
print pascal(1,3) #3
print pascal(2,4) #6
print pascal(2,6)