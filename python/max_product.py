# https://leetcode.com/problems/maximum-product-subarray/
def maxProduct(self, nums: List[int]) -> int:
        m = None
        i = 0
        endEarly = False
        while i < len(nums):
            if m == None:
                m = nums[i]
            m = max(m, nums[i])
            j = i + 1
            prev = nums[i]
            if j < len(nums):
                cur = nums[i] * nums[j]
                while j < len(nums):
                    m = max(m, cur)
                    prev = cur
                    if j +1 < len(nums):
                        cur = prev * nums[j+1]
                    j += 1
            i += 1
        return m
