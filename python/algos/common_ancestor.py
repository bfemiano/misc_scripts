a1 = ("a1", (None, None))
a2 = ("a2", (a1, None))
a3 = ("a3", (a2, None))
a4 = ("a4", (None, None))
a5 = ("a5", (a3, a4))
a6 = ("a6", (None, None))
a7 = ("a7", (None, None))
a8 = ("a8", (a6, a7))
a9 = ("a9", (a8, None))
tree = ("root", (a5, a9))

def grt_common_ancestor(tree, to_find):
    
    r = find_common(tree, to_find, 0)
    print r

def find_common(node, to_find, height):
    height += 1
    id, (l, r) = node
    found = []
    if l is not None:
        if l[0] in to_find:
             found.append(l[0])
        left= find_common(l, to_find, height)
        found.extend(left)
    if r is not None:
        if r[0] in to_find:
            found.append(r[0])
        right = find_common(r, to_find, height)
        found.extend(right)
    if set(found) == to_find:
        return [id, height]
    return found
grt_common_ancestor(tree, set(["a6", "a7"]))
grt_common_ancestor(tree, set(["a1", "a2"]))
grt_common_ancestor(tree, set(["a4", "a9"]))
grt_common_ancestor(tree, set(["a6", "a8"]))