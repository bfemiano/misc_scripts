def ndice(n, seq=""):
    if n == 1:
        for i in range(1, 7):     
            print(seq + str(i))
    else:
        for i in range(1, 7):
            ndice(n-1, seq + str(i))        

#ndice(3) #prints all 216 combintions.

# for [('a', 2), ('b', 2)]
# print
#  [[('a', 1)],
#   [('a', 2)],
#   [('b', 1)],
#   [('b', 2)]
#   [('a', 1), ('b', 1')],
#   [('a', 1), ('b', 2')],
#   [('a', 2), ('b', 1')],
#   [('a', 2), ('b', 2')]]
def combos(pairs):
    def _combos(items, pairs, active):
        for i in range(len(pairs)):
            print(i)
            for letter_pair in pairs[i]:
                items.add(active + (letter_pair))
                _combos(items, pairs[i+1:], active + (letter_pair))
        return items
    start = set([()])
    return _combos(start, [[(p[0], i) for i in range(1, p[1]+1)] for p in pairs], ())

for item in combos([('a', 2), ('b', 2), ('c', 1)]):
    print(item)
