# queue using two stacks
import pytest

class StackQueue:
    
    def __init__(self):
        self.receiver_stack = []
        self.dequeue_stack = []
        
        
    def push(self, item):
        self.receiver_stack.append(item)
    
    
    def next(self):
        if len(self.receiver_stack) == 0:
            return None
        if len(self.dequeue_stack) > 0:
            return self.dequeue_stack.pop()
        else:
            while (len(self.receiver_stack) > 0):
                n = self.receiver_stack.pop()
                self.dequeue_stack.append(n)
            return self.dequeue_stack.pop()
        
        
pytest.main()
        
def test_dequeue_fifo():
    queue = StackQueue()
    queue.push(1)
    queue.push(2)
    queue.push(3)
    assert queue.next() == 1
    
    
def test_dequeue_still_preserves_order():
    queue = StackQueue()
    queue.push(1)
    queue.push(2)
    queue.push(3)
    queue.next()  # 1
    queue.push(4)
    queue.push(5) # should now be [5, ]
    queue.next() == 2
    queue.next() == 3
    queue.next() == 4
    queue.next() == 5
    
def test_empty():
    queue = StackQueue()
    assert queue.next() == None
