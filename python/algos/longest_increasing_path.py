# * Given an integer matrix, find the length of the longest increasing path.
# From each cell, you can either move to four directions: left, right, up or down. You may NOT move diagonally or move outside of the boundary (i.e. wrap-around is not allowed).

# Input: nums = 
# [
#   [9,9,4],
#   [6,6,8],
#   [2,1,1]
# ] 

# Output: 4 
# Explanation: The longest increasing path is [1, 2, 6, 9].

import sys
import pytest


nums = [
 [9, 9, 4],
 [6, 6, 8],
 [2, 1, 1]
]

def search(nums, i, j, path, paths):
    row = nums[i]
    row_val = row[j]
    if i-1 >= 0:
        rotate_val = nums[i-1][j]
        if rotate_val > row_val:
            search(nums, i-1, j, path + [rotate_val], paths)
    if i+1 < len(nums):
        rotate_val = nums[i+1][j]
        if rotate_val > row_val:
            search(nums, i+1, j, path + [rotate_val], paths)
    if j-1 >= 0:
        rotate_val = nums[i][j-1]
        if rotate_val> row_val:
            search(nums, i, j-1, path + [rotate_val], paths)
    if j+1 < len(row):
        rotate_val = nums[i][j+1]
        if rotate_val > row_val:
            search(nums, i, j+1, path + [rotate_val], paths)
    paths.append([i for i in path])

    
def longest_increasing_path(nums):
    paths = []
    for i, row in enumerate(nums):
        for j, row_val in enumerate(row):
            search(nums, i, j, [row_val], paths)

    l = 0
    longest = None
    for p in paths:
        if len(p) > l:
            longest = p
            l = len(p)
    return longest

def test_nums_assignment():
    nums = [
        [9, 9, 4],
        [6, 6, 8],
        [2, 1, 1]
    ]
    assert longest_increasing_path(nums) == [1,2,6,9]


def test_works_not_from_smallest_num():
    nums = [
        [9, 9, 4],
        [10, 6, 8],
        [8, 7, 6]
    ]
    assert longest_increasing_path(nums) == [6,7,8,10]
    
    
def test_simple():
    nums = [
        [1,2]
    ]
    assert longest_increasing_path(nums) == [1,2]
    
    
def test_negative():
    nums = [
        [9, 9, 4],
        [6, 6, 8],
        [2, -1, 1]
    ]
    assert longest_increasing_path(nums) == [-1, 2, 6, 9]
    
        
pytest.main()
