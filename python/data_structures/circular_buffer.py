
class CircularBuffer(object):
    """
        Implement a data structure structure with the following properties:
        1. Initialized to a fixed capacity.
        2. Elements are retrived in the order they are inserted. 
        3. If the structure reaches it's capacity, then overwrite the oldest data in the structure.

        For example:
        capacity = 4
        items inserted: 1 being the oldest, 4 being the most recent. 
            [1, 2, 3, 4]
        inserting 5 would produce:
            [5, 2, 3, 4]
        inserting 6 would produce:
            [5, 6, 3, 4]
        read would then return 3

       Here's the operations the structure should perform:
        1. read(). Retrieve and remove the oldest item inserted into the data structure. If the structure is empty, return -1. 
        2. write(item). Insert an item in the data structure. 
        3. clear(). After this method is called, calls to read() return -1 to signal empty until new writes occur.   
    """

    def __init__(self, capacity):
        self.items = [-1 for i in range(capacity)] # initialize to empty
        self.max_size = capacity
        self.size = 0
        self.read_ptr = 0
        self.write_ptr = 0

    def read(self):
        if self.size == 0:
            return -1
        val = self.items[self.read_ptr]
        self.read_ptr += 1
        self.size -= 1
        if self.read_ptr == self.max_size:
            self.read_ptr = 0
        return val

    def write(self, item):
        if self.write_ptr == self.read_ptr and self.size > 0: # as we overwrite the oldest data, keep the read pointer moving. 
            self.read_ptr += 1
        self.items[self.write_ptr] = item
        self.size += 1
        self.write_ptr += 1
        if self.write_ptr == self.max_size:
            self.write_ptr = 0
        print(self.items)

    def clear(self):
        self.write_ptr = 0
        self.read_ptr = 0
        self.size = 0

    
def test_read_empty():
    buffer = CircularBuffer(4)
    assert buffer.read() == -1
    assert buffer.read() == -1

def test_read_single_insert():
    buffer = CircularBuffer(4)
    buffer.write(1)
    assert buffer.read() == 1

def test_read_multiple_inserts_in_fifo():
    buffer = CircularBuffer(4)
    buffer.write(1)
    buffer.write(2)
    buffer.write(3)
    buffer.write(4)
    assert buffer.read() == 1
    assert buffer.read() == 2
    assert buffer.read() == 3
    assert buffer.read() == 4

def test_buffer_overflow_causes_circular_wrap():
    buffer = CircularBuffer(4)
    buffer.write(1)
    buffer.write(2)
    buffer.write(3)
    buffer.write(4)
    buffer.write(5) # capacity = 4 means 5th insert overwrites oldest insert. Now oldest insert is 2
    assert buffer.read() == 2

def test_clear():
    buffer = CircularBuffer(4)
    buffer.write(1)
    buffer.write(2)
    buffer.clear()
    assert buffer.read() == -1

def test_clear_then_write():
    buffer = CircularBuffer(4)
    buffer.write(1)
    buffer.write(2)
    buffer.clear()
    assert buffer.read() == -1
    buffer.write(1)
    buffer.write(2)
    assert buffer.read() == 1
    assert buffer.read() == 2

def test_interleave_read_writes():
    buffer = CircularBuffer(4)
    buffer.write(1)
    buffer.write(2)
    assert buffer.read() == 1
    assert buffer.read() == 2
    buffer.write(3)
    assert buffer.read() == 3

def test_reads_cannot_go_past_writes():
    buffer = CircularBuffer(4)
    buffer.write(1)
    buffer.write(2)
    buffer.write(3)
    buffer.write(4)
    assert buffer.read() == 1
    assert buffer.read() == 2
    assert buffer.read() == 3
    assert buffer.read() == 4
    assert buffer.read() == -1