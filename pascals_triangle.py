import sys

def get_pascal(col, row):
    if row == 1:
        return [1, 1]
    else:
        lower = get_pascal(col, row-1)
        data = [1]
        for i in range(len(lower)-1):
            data.append(lower[i] + lower[i+1])
        data.append(1)
        return data

def pascal(col, row):
   if row == 0 or row == 1:
       return 1
   else:
       data = get_pascal(col, row)
       return data[col]

print pascal(3,0)
print pascal(0,2) #1
print pascal(1,2) #2
print pascal(1,3) #3
print pascal(2,4) #6
print pascal(2,6)