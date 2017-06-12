t1 = [2, 3]
m = {
    1: ["a", "b", "c"],
    2: ["d", "e", "f"],
    3: ["g", "h", "i"],
}

def get_perms(combos, seq, a):
    if len(a) == 1:
        seq.append(a[0])
        combos.append([b for b in seq])
        seq.pop()
        return combos
    if len(a) == 0:
        return combos
    for i in a:
        seq.append(i)
        remaining = [c for c in a if c != i]
        get_perms(combos, seq, remaining)
        seq.pop()
    return combos
    
def print_combos(seq, p):
    if len(p) == 0:
        print seq
    else:
        for v in m[p[0]]:
            print_combos(seq + v, p[1:])
                
def print_keypad(a):
    combos = []
    for perm in get_perms(combos=[], seq=[], a=a):
        print_combos(seq="", p=perm)
        
print_keypad([1,2])