import sys

def count_change(money, coins):

    def _count(money, coins, cnt):
        if len(coins) == 0 or money < 0:
            return cnt
        if money == 0:
            return cnt + 1

        cnt = _count(money-coins[0], coins, cnt)
        cnt = _count(money, coins[1:], cnt)
        return cnt

    return _count(money, sorted(coins), 0)

print count_change(int(sys.argv[1]), map(int, sys.argv[2].split(',')))