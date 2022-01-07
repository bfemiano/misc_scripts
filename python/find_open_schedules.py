
# find open schedule

# where schedules = 
# [(3.25,9.75)
#  (9.0,11.0),
#  (4.0,5.0)
# ]
import pytest

def findOpenTimes(schedules):

    schedules = sorted(schedules, key=lambda x: x[0])
    available_ranges = []
    scan_index = 0.0
    i = 0
    if schedules[0][0] > 0.0: # assuming the first entry isn't zero itself. 
        available_ranges = [(0, schedules[0][0])] # everything from 0 -> earliest_schedule start time is free. 
        i = 1
    scan_index = schedules[0][1]
    while scan_index <= 12.0 and i < len(schedules):
        s = schedules[i]
        if scan_index < s[0]:
            diff = s[0] - scan_index
            available_ranges.append((scan_index, scan_index + diff))
            scan_index += s[1] - scan_index 
        i += 1
    last_s = schedules[len(schedules)-1]
    if 12.0 - last_s[1] > 0:
        available_ranges.append((last_s[1], 12.0))
    return available_ranges

# (3.25, 9.75), (4.0, 5.0), (9.00, 11.0)
# (3.25, 6), (7, 8)
output = findOpenTimes([(3.25,9.75), (9.0,11.0), (4.0,5.0)]) 

def testOverlapping():
    output = findOpenTimes([(3.25,9.75), (9.0,11.0), (4.0,5.0)]) 
    assert output == [(0, 3.25), (11.0, 12.0)]
    
def testNoneOverlapping():
    output = findOpenTimes([(3.0,4.0), (6.0,7.0), (10.0, 11.0)]) 
    assert output == [(0.0,3.0), (4.0, 6.0), (7.0, 10.0), (11.0, 12.0)]
    
def testOneRange():
    output = findOpenTimes([(0.0, 3.0)]) 
    assert output == [(3.0, 12.0)]
    
def testRangesIncludeEndBound():
    output = findOpenTimes([(0.0, 3.0), (4.0, 12.0)]) 
    assert output == [(3.0, 4.0)]
    
def testSliceInBetweenBounds():
    output = findOpenTimes([(0.0, 3.0), (5.0, 7.0), (7.0, 12.0)]) 
    assert output == [(3.0, 5.0)]
    
def testMultipleWithSameLowerBounds():
    output = findOpenTimes([(0.0, 3.0), (5.0, 7.0), (5.0, 8.0)]) 
    assert output == [(3.0, 5.0), (8.0, 12.0)]

pytest.main()
