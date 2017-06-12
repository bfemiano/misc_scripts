import sys


def is_balanced(cnt, chars):
    if len(chars) == 0:
        return cnt == 0
    c = chars[0]
    if c != '(' and c != ')':
        return is_balanced(cnt, chars[1:])
    elif c == '(':
        cnt += 1
        return is_balanced(cnt, chars[1:])
    else:
        cnt -= 1
        if cnt < 0:
            return False
        return is_balanced(cnt, chars[1:])


print is_balanced(0, sys.argv[1])