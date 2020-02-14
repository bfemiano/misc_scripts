#Python 3.6.7
def flatten(arr_in):
    out = []
    for i in arr_in:
        if isinstance(i, int):
            out.append(i)
        else:
            out.extend(flatten(i))
    return out

print(flatten([1, [2, [3, 4]]])) # [1, 2, 3, 4]
print(flatten([1, [2, 3, [4, 5], 6, [7,8]]])) # [1, 2, 3, 4, 5, 6, 7, 8]