import pytest

def mergeTuples(tups):
    intervals = sorted(intervals, key=lambda x: x[0])
    if len(intervals) == 1:
        return intervals
    i = 1
    merged = []
    item = intervals[0]
    while i < len(intervals):
        next_item = intervals[i]
        if item[1] >= next_item[0]:
            if item[1] >= next_item[1]:
                item = item
            else:
                item = [item[0], next_item[1]]
        else:
            merged.append(item)
            item = next_item
        i += 1
    merged.append(item)
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
