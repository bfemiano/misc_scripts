import pytest

class Node:
    
    def __init__(self, val):
        self.next = None
        self.val = val
        
    
    
def reverse_in_place(n):
    cur = n
    nxt = cur.next
    cur.next = None # this will be the new end, so set it to null. 
    while nxt != None:
        tmp = nxt.next # if a -> b -> c, this will grab c
        nxt.next = cur # now set b.next = a to reverse
        cur = nxt # now set cur = b
        nxt = tmp # now set next = c. Now we have what we need to keep reversing. 
            
    
def setup():
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n5 = Node(5)
    
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n5
    return [n1, n2, n3, n4, n5]    

pytest.main()

def test_reverse():
    [n1, n2, n3, n4, n5] = setup()
    reverse_in_place(n1)
    assert n5.next == n4
    assert n4.next == n3
    assert n3.next == n2
    assert n2.next == n1
    assert n1.next == None
    
def test_single_item():
    n1 = Node(1)
    reverse_in_place(n1)
    assert n1.next == None

    
def test_reverse_partial_list():
    [n1, n2, n3, n4, n5] = setup()
    reverse_in_place(n3)
    assert n5.next == n4
    assert n4.next == n3
    assert n3.next == None
    assert n1.next == n2 # n1 -> n2 is still in order. 
    assert n2.next == n3 # so is n2 -> n3
