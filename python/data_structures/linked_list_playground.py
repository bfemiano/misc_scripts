import pytest

class Node:
    
    def __init__(self, val):
        self.val = val
        self.next = None
    
    
    def insert(self, node):
        tmp = self.next
        self.next = node
        node.next = tmp
    


def ll_remove(start, node_to_remove):
    n = start
    prev = start 
    while n is not None:
        if n == node_to_remove:
            if n.next is not None:
                tmp = n.next
                prev.next = tmp
        prev = n
        n = n.next

        
def ll_insert(node, next_node):
    if node.next is not None:
        tmp = node.next
        node.next = next_node
        next_node.next = tmp
    
    
def reverse(start):
    if start.next is None: # Just one node
        return start
    
    else:
        items = [start]
        cur = start.next
        while cur is not None:
            items.append(cur)
            cur = cur.next

        i = len(items) - 1
        while i >= 0:
            item = items[i]
            if i != 0:
                item.next = items[i-1]
            i -= 1        
    
def reverse_in_place(start):
    if start.next is None:
        return start
    
    def _reverse(node, next_node):
        if next_node.next is not None:
            _reverse(next_node, next_node.next)
        next_node.next = node
    
    _reverse(start, start.next)    
    
def test_reverse_inplace_on_one():
    a = Node("a")
    reverse_in_place(a)
    assert a.next == None
    
    a = Node("a")
    b = Node("b")
    a.next = b
    reverse_in_place(a)
    assert b.next == a
    

def test_reverse_in_place_multiple():
    a = Node("a")
    b = Node("b")
    c = Node("c")
    d = Node("d")
    a.next = b
    b.next = c
    d.next = c
    reverse_in_place(a)
    assert d.next == c
    assert c.next == b
    assert b.next == a
    
    
def test_reverse_works_on_one():
    a = Node("a")
    reverse(a)
    assert a.next == None
    
    a = Node("a")
    b = Node("b")
    a.next = b
    reverse(a)
    assert b.next == a
    
    
def test_reverse_multiple():
    a = Node("a")
    b = Node("b")
    c = Node("c")
    d = Node("d")
    a.next = b
    b.next = c
    d.next = c
    reverse(a)
    assert d.next == c
    assert c.next == b
    assert b.next == a
    

def test_insert():
    a = Node("a")
    b = Node("b")
    c = Node("c")
    d = Node("d")
    e = Node("e")
    f = Node("f")

    a.next = b
    b.next = c
    c.next = d
    d.next = f
    ll_insert(d, e)
    assert a.val == "a"
    assert a.next == b
    assert b.next == c
    assert c.next == d
    assert d.next == e
    assert e.next == f

def test_remove():
    a = Node("a")
    b = Node("b")
    c = Node("c")

    a.next = b
    b.next = c
    ll_remove(a, b)
    assert a.next == c
    
pytest.main()
