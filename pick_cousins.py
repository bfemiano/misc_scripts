import random
cousins = ['Larissa', 'Todd', 'Brian', 'Liz', 'Aiden', 'Andrew', 'Andrew G.', 'Christopher', 'Rachel']

def pick(cousin):
    rand_cousin = cousin
    while rand_cousin == cousin:
        n = random.randint(0, len(cousins)-1)
        rand_cousin = cousins[n]
    return rand_cousin
    

cousins_copy = [c for c in cousins]
assignments = {}
for c in cousins_copy:
    choice = 'N'
    while choice == 'N':
        rand_cousin = pick(c)
        choice = raw_input("Accept %s -> %s? Enter (Y/N) " % (c, rand_cousin))
    cousins.remove(rand_cousin)
    assignments[c] = rand_cousin
    
print assignments