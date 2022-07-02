#https://leetcode.com/problems/plus-one/
def plusOne(self, digits: List[int]) -> List[int]:
        def _plusOne(i):
            d = digits[i]
            if i == len(digits)-1:
                if d + 1 == 10:
                    return [0]
                else:
                    return [d+1]
            else:
                inc = _plusOne(i+1)
                if inc[0] > 0:
                    return [d] + inc
                else:
                    if d + 1 == 10 and digits[i+1] == 9:
                        return [0] + inc
                    elif inc[0] == 0 and digits[i+1] != 0:
                        return [d+1] + inc
                    else:
                        return [d] + inc
        output = _plusOne(0)
        if output[0] == 0:
            output = [1] + output
        return output
