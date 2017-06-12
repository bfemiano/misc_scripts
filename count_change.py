import sys

def count_change_inner(money, coins, combos, active, tried):
    key = tuple(sorted(active))
    if key not in tried:
        if money <= 0:
            if money == 0 and key not in combos:
                combos = frozenset([c for c in combos] + [key])
            return combos
        tried.add(key)
        for coin in coins:
            combos = count_change_inner(money-coin, coins, combos, active + [coin], tried)
    return combos


def count_change(money, coins):
    coins = filter(lambda x: x <= money, coins)
    if len(coins) == 0:
        return 0
    combos = count_change_inner(money, coins, frozenset(), [], set())
    return len(combos)

print count_change(int(sys.argv[1]), map(int, sys.argv[2].split(',')))