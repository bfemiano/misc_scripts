import pytest

def mergeTuples(tups):
    
    tups = sorted(tups, key=lambda x: x[0])
    if len(tups) == 1:
        return tups
    cur_start = tups[0][0]
    cur_end = tups[0][1]
    i = 1
    merged = []
    while i < len(tups):
        next_tup = tups[i]
        if cur_end < next_tup[0]:
            merged.append((cur_start, cur_end))
            cur_start = next_tup[0]
            cur_end = next_tup[1]
        else:
            if next_tup[0] < cur_end < next_tup[1]:
                cur_end = next_tup[1]
        i+=1
    merged.append((cur_start, cur_end))
    return merged
        
    
def test_merge1():
    assert mergeTuples([(1, 2)]) == [(1,2)]
    
def test_mergeTwo():
    assert mergeTuples([(1, 2), (3, 7), (4, 5)]) == [(1, 2), (3, 7)]
    
def test_mergeTwoOutOfOrder():
    assert mergeTuples([(4, 5), (1, 2), (3, 7)]) == [(1, 2), (3, 7)]
    
def test_mergePartialOverlap():
    assert mergeTuples([(1, 2), (3, 7), (6, 8)]) == [(1, 2), (3, 8)]
    
def test_mergeSeveralSameStart():
    assert mergeTuples([(1, 2), (3, 7), (3, 8)]) == [(1, 2), (3, 8)]
    
def test_mergeSeveralMixedOverlap():
    assert mergeTuples([(1, 2), (3, 7), (4, 5), (6, 8)]) == [(1, 2), (3, 8)]
    
def mergeNoneOverlapping():
    assert mergeTuples([(1, 2), (3, 7), (9, 10)]) == [(1, 2), (3, 7), (9, 10)]
    
pytest.main()
