from functools import cmp_to_key

def compare(a, b):
    if a[0] == b[0]:
        if a[1] <= b[1]:
            return -1
        elif a[1] > b[1]:
            return 1
        return 0
    else:
        if a[0] < b[0]:
            return -1
        elif a[0] > b[0]:
            return 1
        return 0


def merge_intervals(a):
    sorted_by_first = sorted(a, key=cmp_to_key(compare))
    print(sorted_by_first)
    l = len(a)
    cur = sorted_by_first[0]
    i = 1
    if l > 0:
        next = sorted_by_first[1]
    else:
        return sorted_by_first
    while (i < l):
        if cur[1] >= next[0]:
            cur[1] = next[1]
        else:
            print(cur)
            cur = next
        i += 1
        if i < l:
            next = sorted_by_first[i]
        elif i == l:
            print(next)


a = [[1, 3], [1, 2], [2, 4]] # becomes [[1, 2], [1, 3], [2, 4]]
merge_intervals(a)

a = [[1, 3], [6, 9], [2, 4]]
merge_intervals(a)


a = [[0, 1], [1, 3], [6, 9], [2, 4]]
merge_intervals(a)

a = [[0, 1], [2, 3], [4, 5], [6, 7]]
merge_intervals(a)

a = [[0, 1], [1, 2], [1, 2]]
merge_intervals(a)
