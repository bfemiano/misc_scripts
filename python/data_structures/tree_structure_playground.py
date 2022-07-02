import pytest


class TreeNode:
    
    def __init__(self, left, right, value):
        self.left = left
        self.right = right
        self.value = value
        
        
class BSTree:
    
    def __init__(self):
        self.root = None
    
    def find(self, value):
        def _find(node):
            if node.value == value:
                return node
            else:
                if node.left == None and node.right == None:
                    return None
                if node.left != None:
                   found_node = _find(node.left)
                   if found_node != None: 
                        return found_node 
                if node.right != None:
                    found_node = _find(node.right)
                    if found_node != None:
                        return found_node
                return None
        return _find(self.root)
    
    def find_node_with_child(self, value):
        def _find(node):
            if node.left == None and node.right == None:
                    return None
            if node.left != None:
                if node.left.value == value:
                    return node
                else:
                    found_node = _find(node.left)
                    if found_node != None: 
                        return found_node 
            if node.right != None:
                if node.right.value == value:
                    return node
                else:
                    found_node = _find(node.right)
                    if found_node != None:
                        return found_node
            return None
        return _find(self.root)
    
    def insert(self, value, left_node=None, right_node=None):
        def _insert(node, value, left_n, right_n):
            if value < node.value:
                if node.left != None:
                    _insert(node.left, value, left_n, right_n)
                else:
                    node.left = TreeNode(left_n, right_n, value)
            else:
                if node.right != None:
                    _insert(node.right, value, left_n, right_n)
                else:
                    node.right = TreeNode(left_n, right_n, value)
            
        if self.root == None:
            self.root = TreeNode(None, None, value)
        else:
            _insert(self.root, value, left_node, right_node)
            
    def delete(self, value):
        node = self.find_node_with_child(value)
        if node != None:
            tmp = None
            if node.left != None and node.left.value == value:
                tmp = node.left
                node.left = None
            else:
                tmp = node.right
                node.right = None
            if tmp.left != None:
                self.insert(tmp.left.value, tmp.left.left, tmp.left.right)
            if tmp.right != None:
                self.insert(tmp.right.value, tmp.right.left, tmp.right.right)
            
def test_delete_node_with_no_children():
    tree = BSTree()
    tree.insert(10)
    tree.insert(4)
    tree.delete(4)
    tree_node = tree.find(10)
    assert tree_node.value == 10
    assert tree_node.left == None
    assert tree_node.right == None
    

def test_delete_node_with_left_child():
    tree = BSTree()
    tree.insert(10)
    tree.insert(9)
    tree.insert(6)
    tree.delete(9)
    tree_node = tree.find(10)
    assert tree_node.value == 10
    assert tree_node.left.value == 6
    assert tree_node.right == None
    

def test_delete_node_with_right_child():
    tree = BSTree()
    tree.insert(10)
    tree.insert(7)
    tree.insert(8)
    tree.delete(7)
    tree_node = tree.find(10)
    assert tree_node.value == 10
    assert tree_node.left.value == 8
    assert tree_node.right == None
    

def test_delete_node_with_two_children():
    tree = BSTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(4)
    tree.insert(6)
    tree.delete(5)
    tree_node = tree.find(10)
    assert tree_node.value == 10
    assert tree_node.left.value == 4
    assert tree_node.left.right.value == 6
    
    
def test_delete_not_root_node_with_two_children():
    tree = BSTree()
    tree.insert(10)
    tree.insert(5)
    tree.insert(6)
    tree.insert(2)
    tree.insert(1)
    tree.insert(4)
    tree.insert(3)
    tree.delete(2)
    tree_node = tree.find(10)
    assert tree_node.left.value == 5
    
    tree_node = tree.find(5)
    assert tree_node.left.value == 1
    assert tree_node.right.value == 6
    
    tree_node = tree.find(1)
    assert tree_node.left == None
    assert tree_node.right.value == 4
    
    tree_node = tree.find(4)
    assert tree_node.left.value == 3
    assert tree_node.right == None

            
def test_find_node_with_child():
    tree = BSTree()
    tree.insert(10)
    tree.insert(4)
    tree_node = tree.find_node_with_child(4)
    assert tree_node.value == 10
    assert tree_node.left.value == 4
    assert tree_node.right == None
            

def test_root():
    tree = BSTree()
    tree.insert(10)
    tree_node = tree.find(10)
    assert tree_node.left == None
    assert tree_node.right == None
    assert tree_node.value == 10
    
def test_root_with_one_terminal_left():
    tree = BSTree()
    tree.insert(10)
    tree.insert(4)
    tree_node = tree.find(4)
    assert tree_node.left == None
    assert tree_node.right == None
    assert tree_node.value == 4
    
def test_root_with_two_children():
    tree = BSTree()
    tree.insert(10)
    tree.insert(4)
    tree.insert(11)
    tree_node = tree.find(10)
    assert tree_node.left.value == 4
    assert tree_node.right.value == 11
    assert tree_node.value == 10
   
def test_tree_with_some_depth():
    tree = BSTree()
    tree.insert(10)
    tree.insert(4)
    tree.insert(11)
    tree.insert(5)
    tree.insert(3)
    tree_node = tree.find(4)
    assert tree_node.left.value == 3
    assert tree_node.right.value == 5
    assert tree_node.value == 4
    
def test_tree_with_more_depth_can_find_left():
    tree = BSTree()
    tree.insert(10)
    tree.insert(6)
    tree.insert(11)
    tree.insert(4)
    tree.insert(3)
    tree.insert(5)
    tree_node = tree.find(4)
    assert tree_node.left.value == 3
    assert tree_node.right.value == 5
    assert tree_node.value == 4
    
    
def test_tree_with_more_depth_can_find_right():
    tree = BSTree()
    tree.insert(10)
    tree.insert(6)
    tree.insert(11)
    tree.insert(16)
    tree.insert(15)
    tree.insert(17)
    tree_node = tree.find(16)
    assert tree_node.left.value == 15
    assert tree_node.right.value == 17
    assert tree_node.value == 16
    
def test_tree_with_depth_found_node_has_one_right_child():
    tree = BSTree()
    tree.insert(10)
    tree.insert(4)
    tree.insert(11)
    tree.insert(5)
    tree_node = tree.find(4)
    assert tree_node.left == None
    assert tree_node.right.value == 5
    assert tree_node.value == 4
    
def test_tree_with_depth_found_node_has_one_left_child():
    tree = BSTree()
    tree.insert(10)
    tree.insert(4)
    tree.insert(11)
    tree.insert(3)
    tree_node = tree.find(4)
    assert tree_node.left.value == 3
    assert tree_node.right == None
    assert tree_node.value == 4
    
def test_left_skewed_tree():
    tree = BSTree()
    tree.insert(10)
    tree.insert(9)
    tree.insert(8)
    tree.insert(4)
    tree.insert(3)
    tree.insert(6)
    tree_node = tree.find(4)
    assert tree_node.left.value == 3
    assert tree_node.right.value == 6
    assert tree_node.value == 4
    
def test_right_skewed_tree():
    tree = BSTree()
    tree.insert(10)
    tree.insert(11)
    tree.insert(12)
    tree.insert(13)
    tree.insert(20)
    tree.insert(15)
    tree.insert(21)
    tree_node = tree.find(20)
    assert tree_node.left.value == 15
    assert tree_node.right.value == 21
    assert tree_node.value == 20

def test_tree_handles_same_values_by_placing_right():
    tree = BSTree()
    tree.insert(10)
    tree.insert(9)
    tree.insert(8)
    tree.insert(8)
    tree.insert(7)
    tree_node = tree.find(8)
    assert tree_node.left.value == 7
    assert tree_node.right.value == 8
    assert tree_node.value == 8
    
    
def test_tree_can_handle_not_finding():
    tree = BSTree()
    tree.insert(10)
    tree.insert(4)
    tree.insert(11)
    tree.insert(5)
    tree.insert(3)
    tree_node = tree.find(2)
    assert tree_node == None
    
pytest.main(["-s"])
