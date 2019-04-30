HW_SOURCE_FILE = 'hw03.py'

#############
# Questions #
#############

def cons(left, right):
    return (left, right)

def left(pair):
    return pair[0]

def right(pair):
    return pair[1]

from fractions import gcd

def make_rat(n, d):
    """The rational number n/d, assuming n, d are integers, d!=0"""
    g = gcd(n, d) if d > 0 else -gcd(n, d)
    n //= g; d //= g
    return cons(n, d)

def numer(r):
    """The numerator of rational number r."""
    return left(r)

def denom(r):
    """The denominator of rational number r."""
    return right(r)

def add_rat(x, y):
    return make_rat(numer(x) * denom(y) + numer(y) * denom(x),
                    denom(x) * denom(y))

def mul_rat(x, y):
    """The product of rational numbers x and y."""
    return make_rat(numer(x) * numer(y), denom(x) * denom(y))

def div_rat(x, y):
    """The quotient of rationals x/y.
    >>> a, b = make_rat(3, 4), make_rat(5, 3)
    >>> c = div_rat(a, b)
    >>> numer(c)
    9
    >>> denom(c)
    20
    """
    return make_rat(numer(x) * denom(y), denom(x) * numer(y))

def lt_rat(x, y):
    """Returns True iff x < y as rational numbers; else False.
    >>> a, b = make_rat(6, 7), make_rat(12, 16)
    >>> lt_rat(a, b)
    False
    >>> lt_rat(b, a)
    True
    >>> lt_rat(a, b)
    False
    >>> a, b = make_rat(-6, 7), make_rat(-12, 16)
    >>> lt_rat(a, b)
    True
    >>> lt_rat(b, a)
    False
    >>> lt_rat(a, a)
    False
    """
    return numer(x) / denom(x) < numer(y) / denom(y)

def has_seven(k):
    """Returns True if at least one of the digits of k is a 7, False otherwise.

    >>> has_seven(3)
    False
    >>> has_seven(7)
    True
    >>> has_seven(7)
    True
    >>> has_seven(2634)
    False
    >>> has_seven(734)
    True
    >>> has_seven(7777)
    True
    """
    "*** YOUR CODE HERE ***"
    if k == 0:
        return False
    elif k%10 == 7:
        return True
    else:
        return has_seven(k // 10)

def pingpong(n):
    """Return the nth element of the ping-pong sequence.

    >>> pingpong(7)
    7
    >>> pingpong(8)
    6
    >>> pingpong(15)
    1
    >>> pingpong(21)
    -1
    >>> pingpong(22)
    0
    >>> pingpong(30)
    6
    >>> pingpong(68)
    2
    >>> pingpong(69)
    1
    >>> pingpong(70)
    0
    >>> pingpong(71)
    1
    >>> pingpong(72)
    0
    >>> pingpong(100)
    2
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'pingpong', ['Assign', 'AugAssign'])
    True
    """
    def helper(ind, val, op):
        if ind == n:
            return val + op
        elif has_seven(ind) or ind % 7 == 0:
            return helper(ind + 1, val + op, op * -1)
        else:
            return helper(ind + 1, val + op, op)
    return helper(1,0,1)
# Linked List definition
empty = 'empty'

def is_link(s):
    """s is a linked list if it is empty or a (first, rest) pair."""
    return s == empty or (type(s) == list and len(s) == 2 and is_link(s[1]))


def link(first, rest=empty):
    """Construct a linked list from its first element and the rest."""
    assert is_link(rest), 'rest must be a linked list.'
    return [first, rest]


def first(s):
    """Return the first element of a linked list s."""
    assert is_link(s), 'first only applies to linked lists.'
    assert s != empty, 'empty linked list has no first element.'
    return s[0]


def rest(s):
    """Return the rest of the elements of a linked list s."""
    assert is_link(s), 'rest only applies to linked lists.'
    assert s != empty, 'empty linked list has no rest.'
    return s[1]

def isempty(s):
    """Returns True iff s is the empty list."""
    return s is empty


def print_link(s):
    """Print elements of a linked list s.

    >>> s = link(1, link(2, link(3, empty)))
    >>> print_link(s)
    1 2 3
    """
    line = ''
    while s != empty:
        if line:
            line += ' '
        line += str(first(s))
        s = rest(s)
    print(line)

def change(lst, s, t):
    """Returns a link matching lst but with all instances of s (if any)
    replaced by t.

    >>> lst = link(1, link(2, link(3)))
    >>> new = change(lst, 3, 1)
    >>> print_link(new)
    1 2 1
    >>> newer = change(new, 1, 2)
    >>> print_link(newer)
    2 2 2
    >>> newest = change(newer, 5, 1)
    >>> print_link(newest)
    2 2 2
    """
    if isempty(lst):
        return lst
    elif first(lst) == s:
        return link(t, change(rest(lst), s, t))
    else:
        return link(first(lst), change(rest(lst), s, t))

def insert_at_end(lst, elem):
    """Return a linked list that is the same as lst with elem added
    at the end.

    >>> lst1 = insert_at_end(empty, 1)
    >>> print_link(lst1)
    1
    >>> lst2 = insert_at_end(lst1, 2)
    >>> print_link(lst2)
    1 2
    >>> lst3 = insert_at_end(lst2, 3)
    >>> print_link(lst3)
    1 2 3
    """
    if isempty(lst):
        return link(elem)
    return link(first(lst), insert_at_end(rest(lst), elem))

def deep_len(lnk):
    """ Returns the deep length of a possibly deep linked list of integers.
    >>> deep_len(link(1, link(2, link(3, empty))))
    3
    >>> deep_len(link(link(1, link(2, empty)), link(3, link(4, empty))))
    4
    >>> deep_len(link(link(link(1, link(2, empty)), \
            link(3, empty)), link(link(4, empty), link(5, empty))))
    5
    """
    if type(first(lnk)) == int and isempty(rest(lnk)):
        return 1
    elif type(first(lnk)) == int and is_link(rest(lnk)):
        return 1 + deep_len(rest(lnk))
    else:
        return deep_len(first(lnk)) + deep_len(rest(lnk))

def flatten(lst):
    """Returns a flattened version of lst.

    >>> flatten([1, 2, 3])     # normal list
    [1, 2, 3]
    >>> x = [1, [2, 3], 4]      # deep list
    >>> flatten(x)
    [1, 2, 3, 4]
    >>> x = [[1, [1, 1]], 1, [1, 1]] # deep list
    >>> flatten(x)
    [1, 1, 1, 1, 1, 1]
    """
    flat = []

    def helper(helper_lst, helper_ind):
        if helper_ind >= len(helper_lst):
            return flat
        if type(helper_lst[helper_ind]) == int:
                flat.append(helper_lst[helper_ind])
        if type(helper_lst[helper_ind]) == list:
                helper(helper_lst[helper_ind], 0)
        return helper(helper_lst, helper_ind + 1)

    return helper(lst, 0)

def riffle(deck):
    """Produces a single, perfect riffle shuffle of DECK, consisting of
    DECK[0], DECK[M], DECK[1], DECK[M+1], ... where M is position of the
    second half of the deck.  Assume that len(DECK) is even.
    >>> riffle([3, 4, 5, 6])
    [3, 5, 4, 6]
    >>> riffle(range(20))
    [0, 10, 1, 11, 2, 12, 3, 13, 4, 14, 5, 15, 6, 16, 7, 17, 8, 18, 9, 19]
    """
    "*** YOUR CODE HERE ***"
    lst = []
    for ind in range(int(len(deck) / 2)):
            lst.append(deck[ind])
            lst.append(deck[int(ind + (len(deck) / 2))])
    return lst

def tree(label, branches=[]):
    for branch in branches:
        assert is_tree(branch), 'branches must be trees'
    return [label] + list(branches)

def label(tree):
    return tree[0]

def branches(tree):
    return tree[1:]

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True

def is_leaf(tree):
    return not branches(tree)

def print_tree(t, indent=0):
    """Print a representation of this tree in which each node is
    indented by two spaces times its depth from the label.

    >>> print_tree(tree(1))
    1
    >>> print_tree(tree(1, [tree(2)]))
    1
      2
    >>> numbers = tree(1, [tree(2), tree(3, [tree(4), tree(5)]), tree(6, [tree(7)])])
    >>> print_tree(numbers)
    1
      2
      3
        4
        5
      6
        7
    """
    print('  ' * indent + str(label(t)))
    for b in branches(t):
        print_tree(b, indent + 1)

def build_binary_ones(h):
    """
    >>> print_tree(build_binary_ones(1))
    1
      1
      1
    >>> print_tree(build_binary_ones(2))
    1
      1
        1
        1
      1
        1
        1
    """
    if h == 0:
        return tree(1)
    return tree(1, [build_binary_ones(h -1), build_binary_ones(h - 1)])
    
        

def build_ones(h, branching_factor=2):
    """
    >>> print_tree(build_ones(2))
    1
      1
        1
        1
      1
        1
        1
    >>> print_tree(build_ones(3, 1))
    1
      1
        1
          1
    """
    if h == 0:
        return tree(1)
    return tree(1, [build_ones(h -1, branching_factor)] * branching_factor)