'''
Design a data structure that supports all following operations in O(1) time.

insert(val): Inserts an item val to the set if not already present.
remove(val): Removes an item val from the set if present.
getRandom: Returns a random element from current set of elements. Each element must have the same probability of being returned.
'''
from random import randint
import pytest

class RandomizedSet(object):
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.data = dict()
        self.data_list = []
        
    def insert(self, val):
        """
        Inserts a value to the set. Returns true if the set did not already contain the specified element.
        :type val: int
        :rtype: bool
        """
        added = False
        if val not in self.data.keys():
            added = True
            self.data_list.append(val)
            self.data[val] = len(self.data_list) - 1
        return added
        
    def remove(self, val):
        """
        Removes a value from the set. Returns true if the set contained the specified element.
        :type val: int
        :rtype: bool
        """
        contained = False
        if val in self.data.keys():
            contained = True
            index = self.data[val]
            last = self.data_list[len(self.data)-1]
            self.data_list[index] = last
            self.data_list.pop()
            self.data[last] = index
            del self.data[val]
            # [1 2 3 4 5]
            # [1 2 3 4 5 6 7 8]
            # [1 2 3 4 8 6 7]
        return contained

    def getRandom(self):
        """
        Get a random element from the set.
        :rtype: int
        """
        index = randint(0, len(self.data.keys())-1)
        return self.data_list[index]
  
pytest.main()


def test_insert():
    rs = RandomizedSet()
    added = rs.insert(5)
    assert added == True
    added = rs.insert(5)
    assert added == False
    
def test_remove_tail():
    rs = RandomizedSet()
    rs.insert(4)
    rs.insert(6)
    found = rs.remove(5)
    assert found == False
    rs.insert(5)
    found = rs.remove(5)
    assert found == True
    assert rs.data == {4: 0, 6: 1}
        
def test_remove_midway():
    rs = RandomizedSet()
    rs.insert(1)
    rs.insert(2)
    rs.insert(3)
    rs.insert(4)
    rs.insert(5)
    rs.remove(3)
    assert rs.data == {1: 0, 2: 1, 5: 2, 4: 3}
    
def test_get_random():
    rs = RandomizedSet()
    rs.insert(1)
    rs.insert(2)
    rs.insert(3)
    rs.insert(4)
    rs.insert(5)
    val = rs.getRandom()
    assert val != None
