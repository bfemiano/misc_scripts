import sys


def is_balanced(cnt, chars):
    if len(chars) == 0:
        return cnt == 0
    if chars[0] != '(' and chars[0] != ')':
        return is_balanced(cnt, chars[1:])
    elif chars[0] == '(':
        return is_balanced(cnt + 1, chars[1:])
    else:
        if cnt -1 < 0:
            return False
        return is_balanced(cnt - 1, chars[1:])


print is_balanced(0, sys.argv[1])