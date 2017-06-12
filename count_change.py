import sys

def count_change_inner(money, coins, combos, active):
    if len(coins) == 0:
        return 0
    if not (tuple(sorted(active)), False) in combos:
        if money <= 0:
            if money == 0:
                combos.add((tuple(sorted(active)), True))
            return combos
        combos.add((tuple(sorted(active)), False))

        def _count(coin):
            count_change_inner(money-coin, coins, combos, active + [coin])
        map(_count, coins)
    return combos


def count_change(money, coins):
    return len(filter(lambda c: c[1], count_change_inner(money, filter(lambda x: x <= money, coins), set(), [])))

print count_change(int(sys.argv[1]), list(reversed(sorted(map(int, sys.argv[2].split(','))))))