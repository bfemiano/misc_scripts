import copy
from functools import cmp_to_key

__author__ = 'bfemiano'
import sys


def collect_patterns(stream=sys.stdin, num_patterns=0):
    """Returns a set of all patterns.

    stream -> input stream to read pattern lines.
    num_patterns -> upper bound on number of lines to read from stream.

    Given an input stream and a number of lines to read, parse each line
    and store into the pattern set. Replace ',' with '/' and remove newlines
    before insertion.
    """
    patterns = set()
    for i in xrange(0, num_patterns):
        key = stream.readline().strip('\n').replace(',', '/')
        patterns.add(key)
    return patterns


def cmp_by_cnt_then_order(x, y):
    """ Comparison function used by sorted() to organize wildcard combinations
        as strings.

        x, y -> unique combination strings where x != y.
        The usage in 'build_wildcard_combinations()' promises this condition.
        A check for this condition still occurs incase this function is reused
        elsewhere.

        Patterns with fewer '*' occurrences sort before those with more.
        If two patterns contain the same number of '*' occurrences, sort based
        on '*' character positioning. Patterns where the leftmost occurrence of '*' appears
        further right will sort before those with the same number of '*' occurrences.
        (ex. 'a.*.*' will sort '*.b.*', which sorts before '*.*.c')
    """
    if x == y:
        raise RuntimeError(x + ' and ' + y + ' cannot be equal.')
    if x.count('*') < y.count('*'):
        return -1
    elif x.count('*') > y.count('*'):
        return 1
    else:
        #find the earliest position of a wildcard, or -1.)
        pos_x = x.find('*')
        pos_y = y.find('*')
        return 1 if pos_x < pos_y else -1


def build_wildcard_combinations(path):
    """Take a given path and build every combination of
        possible wildcard configurations at every position in the path.

        path -> full path string used to generation combinations (ex. 'foo/bar/baz')

        A path of length 'k' will explode out to 2^k possible wildcard matches.
        ex. path = 'a.b', len(key) = 2 and will produce a potential solutions
        vector of 'a.b', 'a.*', '*.b', and '*.*'.

        The performance of this function is exponential with respect to the number of
        path elements. It operates very well with paths <10.
        (I.E. where combinations of wildcards <= 1024).

        To accomplish this, build an array of path elements split on '/'.
        Initialize the first 2 entries. For each index from 1
        through the length of the path elements,
        duplicate every combination in the solution vector.
        This will increase the complete solution vector each time by a
        factor of 2. After duplication, for each combination in the vector,
        alternate insertion between the path element at position 'index'
        and a wildcard. This insures every possible combination is
        eventually generated for paths of arbitrary length.

        The combinations are sorted based on the comparison function
        'cmp_by_cnt_then_order()' and then returned as a sorted list of
        strings. Each string represents a '/' separated path.
    """
    parts = path.split('/')
    #initialize the combinations for the first position at index = 0.
    solutions = [[parts[0]], ['*']]
    for index in range(1, len(parts)):
        #inefficient to copy at each step, but makes the logic somewhat easier to follow.
        temp = copy.copy(solutions)
        solutions = []
        for item in temp:
            solutions.append(item)
            solutions.append(copy.copy(item))
        j = 0
        #alternate between the exact match element and '*' for combination generation.
        for item in solutions:
            if j % 2 == 0:
                item.append(parts[index])
            else:
                item.append('*')
            j += 1
    #join the each combination as a '/' separated path string before sorting.
    ordered_combos=sorted(map(lambda x: '/'.join(x), solutions),
                          key=cmp_to_key(cmp_by_cnt_then_order))
    return ordered_combos


def match_paths_to_patterns(stream=sys.stdin, num_paths=0, patterns=set()):
    """Read paths from stdin. Apply the best matching pattern, or print 'NO MATCH' if none found.

        stream -> input stream to read paths.
        num_paths -> upper bound on the number of lines to read from stream.
        patterns -> set of all unique patterns to compare each path against.

        Compare each path against the sorted list of possible wildcard combinations until
        a match is found. The combinations are sorted in order based on the precedence
        rules for this assignment, therefore the first match, if any, is the best.

        Otherwise print 'NO MATCH' if no combination of wildcards and path elements exists in the pattern set.

        Given 'N' patterns, 'M' paths, and some constant time 'k' that corresponds to the various
        combination sorting and generation operations,
        this solution is worst case O(N + k) efficiency, which reduces down to O(N).
        This is much better than the quadratic version of O(N*M). Instead of checking
        against every pattern exhaustively, the program only checks against possible
        wildcard configurations of the path that may or may not be represented as a pattern.

        Assuming you can fit the entire pattern set into memory (a current limitation)
        this algorithm performs the path comparisons much more efficiently than the quadratic solution,
        particularly for somewhat 'narrow' paths of length where the number of directories <= 10.
    """
    for i in xrange(0, num_paths):
        path = stream.readline().strip('\n').rstrip('/').lstrip('/')
        if path in patterns:
            print path.replace('/', ',')
        else:
            ordered_combos = build_wildcard_combinations(path)
            for combo in ordered_combos:
                if combo in patterns:
                    print combo.replace('/', ',')
                    break
            else:
                print 'NO MATCH' + str(i)


def main():
    """Read lines from stdin, construct pattern set, and match paths against patterns.
        1) Read the number of patterns.
        2) Collect all the patterns.
        3) Read the number of paths.
        4) Read each path and apply the best matching, if any, pattern.

        Type conversion errors with the num_patterns and num_paths lead
        to a printout before raising the exception. All other errors raise
        the exception after printing the stack trace.
    """
    try:
        stream = sys.stdin
        num_patterns = int(stream.readline())
        patterns = collect_patterns(stream=stream,
                                    num_patterns=num_patterns)
        num_paths = int(stream.readline())
        match_paths_to_patterns(stream=stream,
                                num_paths=num_paths,
                                patterns=patterns)
    except ValueError:
        print("Malformed path and/or pattern entries. Check your input")
        raise
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
if __name__ == "__main__":
    main()

