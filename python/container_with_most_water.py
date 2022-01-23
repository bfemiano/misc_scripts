# from https://leetcode.com/problems/container-with-most-water/ 
# solution: https://www.code-recipe.com/post/container-with-most-water
def maxArea(self, height: List[int]) -> int:
	m = -1
        i = 0
        j = len(height)-1
        while i != j:
            #print("%i %i" % (i, j))
            head = height[i]
            tail = height[j]
            #print("%i %i" % (head, tail))
            w = j - i
            l = min(head, tail)
            #print("%i %i" % (w, l))
            #print("------")
            m = max(m, l * w)
            if head > tail:
                j -= 1
            else:
                i += 1
        return m


