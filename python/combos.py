def ndice(n, item, items):
    if n == 1:
        for i in range(1, 7):
            items.append(item + [i])
    else:
        for i in range(1, 7):
            ndice(n-1, item + [i], items)
    return items
        
items = ndice(2, [], [])
for combo in items:
    print(combo)
