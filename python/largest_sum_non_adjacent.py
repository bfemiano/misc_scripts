import sys
a = [1, 2, -3, 5, 7]
m = 0 - sys.maxint
seq = []
for i in range(len(a)):
    s = a[i]
    if s > m:
        seq = [a[i]]
        m = s
    j = 0
    prev = i
    while j < len(a):
        if abs(i - j) >= 2:
            if a[i] + a[j] > m:
                m = a[i] + a[j]
                seq = [a[i], a[j]]
            if  abs(j - prev) >= 2:
                s += a[j]
                if s > m:
                    m = s
                    seq.append(a[j])
                prev = j 
        j += 1
print m, seq
                