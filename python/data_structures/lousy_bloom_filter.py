class LousyBloomFilter(object):
    """
        Let's implement a data structure that checks for hash containment in constant time without having to store all the hashes. 
        To accomplish this, we're allowed the potential for slight error. 
        
        The structure can sometimes say a hash is present when it's actually not (false positive), 
           but it should never say a hash wasn't present when it actually was (false negative).

        Assume hashs are integers >= 0. 
        
        Functions: 
            1. add(hash)
                Add the hash to the structure. 

            1. contains(hash)
                If it returns True, there's a chance it might not actually contain the hash.  (False positive)
                If it returns False, then it definitely did not contain the hash. 
    """

    def __init__(self, capacity):
        self.bit_vector = [False for _ in range(capacity)]
        self.capacity = capacity

    def add(self, hash):
        self.bit_vector[hash % self.capacity] = True

    def contains(self, hash):
        return self.bit_vector[hash % self.capacity]

def test_no_collisions_means_100perc_accuracy():
    bloom = LousyBloomFilter(5)
    bloom.add(0)
    bloom.add(4)
    assert list(map(int, bloom.bit_vector)) == [1, 0, 0, 0, 1]
    assert bloom.contains(0)
    assert bloom.contains(4)
    assert not bloom.contains(1)

def test_false_positives_when_collisions():
    bloom = LousyBloomFilter(5)
    bloom.add(0)
    bloom.add(6)
    assert list(map(int, bloom.bit_vector)) == [1, 1, 0, 0, 0] # 6 was indexed at 1 in the vector, so checking for 1 will now yield a false positive.
    assert bloom.contains(0)
    assert bloom.contains(6)
    assert bloom.contains(1) # false positive. Allowable for bloom filter. 
