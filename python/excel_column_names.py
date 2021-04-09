import string
from unittest2 import TestCase
chars = string.uppercase
    
def prnt(seq, n):
    items = []
    if n > 0:
        for k in range(len(chars)):
            items += prnt(seq + chars[k], n-1)
    else:
        for j in range(len(chars)):
             items += [seq + chars[j]]
    return items
    
def start(n):
    items = []
    for i in range(n):
        items += prnt("", i)
    return items
                    
class ArrayIndexToSpreadsheetColumnNameTest(TestCase):

    def test1(self):
            index_map = start(n=1)
            self.assertEqual(len(index_map), 26)
            self.assertEqual(index_map[0], 'A')
            self.assertEqual(index_map[9], 'J')
            self.assertEqual(index_map[25], 'Z')
            
    
    def test2(self):
            '''
                26^2 = 676
                first 26 entries + 676 means that final cell for
                2 char column names will be in 702.
            '''
            index_map = start(n=2)
            self.assertEqual(len(index_map), 702)
            self.assertEqual(index_map[0], 'A')
            self.assertEqual(index_map[25], 'Z')
            self.assertEqual(index_map[26], 'AA')
            self.assertEqual(index_map[701], 'ZZ')
            
    def test3(self):
            '''
                Test 3 char column naming.
                (26 * 26 * 26) + (26 * 26) + 26
                18278
            '''
            index_map = start(n=3)
            self.assertEqual(len(index_map), 18278)
            self.assertEqual(index_map[0], 'A')
            self.assertEqual(index_map[25], 'Z')
            self.assertEqual(index_map[26], 'AA')
            self.assertEqual(index_map[702], 'AAA')
            self.assertEqual(index_map[703], 'AAB')