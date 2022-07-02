# https://leetcode.com/problems/longest-substring-without-repeating-characters/solution/
def lengthOfLongestSubstring(self, s: str) -> int:
        m = 0
        l = len(s)
        i = 0
        while l > i:
            start = 0
            end = l
            #print(end)
            while (start + l) <= len(s):
                sub = s[start:end]
                #print(sub)
                seen = set()
                for c in sub:
                    seen.add(c)
                if len(seen) == l:
                    return l
                start += 1
                end += 1
            # if end > len(s):
            #     end -= l
            #     last_sub = s[end:]
            #     seen = set()
            #     for c in sub:
            #         seen.add(c)
            #     if seen.size() == l:
            #         m = max(l, last_sub)
            l -= 1
        return m
