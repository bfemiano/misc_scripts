# https://leetcode.com/problems/maximum-subarray/
def maxSubArray(self, nums: List[int]) -> int:
        s = 0
        m = -sys.maxsize
        for i in range(0, len(nums)):
            s += nums[i]
            m = max(s, m)
            if s < 0:
                s = 0
        return m
