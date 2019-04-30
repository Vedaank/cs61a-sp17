HW_SOURCE_FILE = 'hw04.py'

############
# Vitamins #
############

def make_counter():
    """Return a counter function.

    >>> c = make_counter()
    >>> c('a')
    1
    >>> c('a')
    2
    >>> c('b')
    1
    >>> c('a')
    3
    >>> c2 = make_counter()
    >>> c2('b')
    1
    >>> c2('b')
    2
    >>> c('b') + c2('b')
    5
    """
    nums = {}
    def counter(key):
        nums[key] = nums.get(key, 0) + 1
        return nums[key]
    return counter

def make_fib():
    """Returns a function that returns the next Fibonacci number
    every time it is called.

    >>> fib = make_fib()
    >>> fib()
    0
    >>> fib()
    1
    >>> fib()
    1
    >>> fib()
    2
    >>> fib()
    3
    >>> fib2 = make_fib()
    >>> fib() + sum([fib2() for _ in range(5)])
    12
    """
    cur, next = 0, 1
    
    def fib():
        nonlocal cur, next
        result = cur
        cur, next = next, cur + next
        return result
    
    return fib

###################
# Towers of Hanoi #
###################

def print_move(origin, destination):
    """Print instructions to move a disk."""
    print("Move the top disk from rod", origin, "to rod", destination)

def move_stack(n, start, end):
    """Print the moves required to move n disks on the start pole to the end
    pole without violating the rules of Towers of Hanoi.

    n -- number of disks
    start -- a pole position, either 1, 2, or 3
    end -- a pole position, either 1, 2, or 3

    There are exactly three poles, and start and end must be different. Assume
    that the start pole has at least n disks of increasing size, and the end
    pole is either empty or has a top disk larger than the top n start disks.

    >>> move_stack(1, 1, 3)
    Move the top disk from rod 1 to rod 3
    >>> move_stack(2, 1, 3)
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 3
    >>> move_stack(3, 1, 3)
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 1 to rod 2
    Move the top disk from rod 3 to rod 2
    Move the top disk from rod 1 to rod 3
    Move the top disk from rod 2 to rod 1
    Move the top disk from rod 2 to rod 3
    Move the top disk from rod 1 to rod 3
    """
    assert 1 <= start <= 3 and 1 <= end <= 3 and start != end, "Bad start/end"
    extra = 6 - start - end
    def helper(n, start, end, extra):
        if n > 0:
            helper(n - 1, start, extra, end)
            print_move(start, end)
            helper(n - 1, extra, end, start)
	
    helper(n, start, end, extra)

###########
# Mobiles #
###########

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

def mobile(left, right):
    """Construct a mobile from a left side and a right side."""
    return tree(None, [left, right])

def sides(m):
    """Select the sides of a mobile."""
    return branches(m)

def side(length, mobile_or_weight):
    """Construct a side: a length of rod with a mobile or weight at the end."""
    return tree(length, [mobile_or_weight])

def length(s):
    """Select the length of a side."""
    return label(s)

def end(s):
    """Select the mobile or weight hanging at the end of a side."""
    return branches(s)[0]

def weight(size):
    """Construct a weight of some size."""
    assert size > 0
    return tree(size)

def size(w):
    """Select the size of a weight."""
    return label(w)

def is_weight(w):
    """Whether w is a weight, not a mobile."""
    return is_leaf(w)

def examples():
    t = mobile(side(1, weight(2)),
               side(2, weight(1)))
    u = mobile(side(5, weight(1)),
               side(1, mobile(side(2, weight(3)),
                              side(3, weight(2)))))
    v = mobile(side(4, t), side(2, u))
    return (t, u, v)


def total_weight(m):
    """Return the total weight of m, a weight or mobile.

    >>> t, u, v = examples()
    >>> total_weight(t)
    3
    >>> total_weight(u)
    6
    >>> total_weight(v)
    9
    """
    if is_weight(m):
        return size(m)
    else:
        return sum([total_weight(end(s)) for s in sides(m)])

def balanced(m):
    """Return whether m is balanced.

    >>> t, u, v = examples()
    >>> balanced(t)
    True
    >>> balanced(v)
    True
    >>> w = mobile(side(3, t), side(2, u))
    >>> balanced(w)
    False
    >>> balanced(mobile(side(1, v), side(1, w)))
    False
    >>> balanced(mobile(side(1, w), side(1, v)))
    False
    """
    if is_weight(m):
        return True
    else:
        left, right = sides(m)
        left_side, right_side = end(left), end(right)
        left_torque = total_weight(left_side) * length(left)
        right_torque = total_weight(right_side) * length(right)
        return balanced(left_side) and balanced(right_side) and left_torque == right_torque

def with_totals(m):
    """Return a mobile with total weights stored as the label of each mobile.

    >>> t, _, v = examples()
    >>> label(with_totals(t))
    3
    >>> print(label(t))                           # t should not change
    None
    >>> label(with_totals(v))
    9
    >>> [label(end(s)) for s in sides(with_totals(v))]
    [3, 6]
    >>> [label(end(s)) for s in sides(v)]         # v should not change
    [None, None]
    """
    if is_weight(m):
        return m
    ends = [with_totals(end(s)) for s in sides(m)]
    total = sum([label(s) for s in ends])
    return tree(total, [side(length(s), t) for s, t, in zip(sides(m), ends)])    

#############
# Intervals #
#############


class interval:
    """A range of floating-point values.

    >>> a = interval(1, 4)
    >>> a
    interval(1, 4)
    >>> print(a)
    (1, 4)
    >>> a.low()
    1
    >>> a.high()
    4
    >>> a.width()
    3
    >>> b = interval(2, -2)  # Order doesn't matter
    >>> print(b, b.low(), b.high())
    (-2, 2) -2 2
    >>> a + b
    interval(-1, 6)
    >>> a - b
    interval(-1, 6)
    >>> a * b
    interval(-8, 8)
    >>> b / a
    interval(-2.0, 2.0)
    >>> a / b
    ValueError
    >>> -a
    interval(-4, -1)
    >>> c = interval(2, 8)
    >>> c + c
    interval(4, 16)
    >>> c - c
    interval(-6, 6)
    >>> c / c
    interval(0.25, 4.0)
    """

    # In all methods below, use the following method to create new intervals.
    # For example, if a method must return interval(x, y), have it
    # return self.makeinterval(x, y) instead.
    def make_interval(self, low, high):
        """Returns an interval of the same type as SELF with bounds LOW
        and HIGH.  Thus, if SELF is an interval, returns interval(LOW, HIGH)."""
        return interval(low, high)

    def __init__(self, low, high):
        self.low_val = min(low, high)
        self.high_val = max(low, high)

    def low(self):
        return (self.low_val)
    
    def high(self):
        return (self.high_val)

    def width(self):
        return self.high() - self.low()

    def __add__(self, other):
        return self.make_interval(self.low() + other.low(), self.high() + other.high())
        
    def __sub__(self, other):
        return self.make_interval(self.low() - other.high(), self.high() - other.low())

    def __mul__(self, other):
        combo1 = self.high() * other.high()
        combo2 = self.high() * other.low()
        combo3 = self.low() * other.high()
        combo4 = self.low() * other.low()
        return self.make_interval(min(combo1, combo2, combo3, combo4), max(combo1, combo2, combo3, combo4))

    def __truediv__(self, other):
        if other.low() <= 0 < other.high():
            raise ValueError
        elif self == other:
            return self.make_interval(self.low() / other.high(), self.high() / other.low())
        else:
            lower = [self.low(), other.low()]
            higher = [self.high(), other.high()]
            return self.make_interval(min(lower) / max(lower), max(higher) / min(higher))

    def __repr__(self):
        return "interval({0}, {1})".format(self.low(), self.high())

    def __str__(self):
        return "({0}, {1})".format(self.low(), self.high())

    def __neg__(self):
        return self.make_interval(-1 * self.low(), -1 * self.high())

class centered_interval(interval):

    def __init__(self, c, tol = None):
        """Initialize SELF to C +- TOL.  TOL is None, then C is assumed to be
        an interval, and SELF will be set to have the same bounds.
        >>> a = centered_interval(1, 2)
        >>> a.low()
        -1
        >>> a.high()
        3
        >>> a.width()
        4
        >>> b = centered_interval(3, 1)
        >>> a + b
        centered_interval(4.0, 3.0)
        >>> a * b
        centered_interval(4.0, 8.0)
        >>> -a
        centered_interval(-1.0, 2.0)
        """
        if tol is None:
            interval.__init__(self, c.low(), c.high())
        else:
            interval.__init__(self, c - tol, c + tol)

    def make_interval(self, low, high):
        """Returns a centered interval whose bounds are LOW and HIGH."""
        return centered_interval(interval(low, high))

    def center(self):
        """The center of SELF.
        >>> centered_interval(5, 1).center()
        5.0
        >>> centered_interval(interval(4, 6)).center()
        5.0
        """
        return float((self.low() + self.high()) / 2)

    def tolerance(self):
        """The tolerance of SELF.
        >>> centered_interval(5, 1).tolerance()
        1.0
        >>> centered_interval(interval(4, 6)).tolerance()
        1.0
        """
        return float(self.width() / 2)

    def __str__(self):
        """A string representation of SELF as center +/- tolerance.
        >>> print(centered_interval(5, 1))
        5.0 +/- 1.0
        >>> print(centered_interval(interval(4, 6)))
        5.0 +/- 1.0
        """
        return "{0} +/- {1}".format(float(self.center()), float(self.tolerance()))

    def __repr__(self):
        """A string represention of a Python expression that will produce SELF.
        >>> centered_interval(5, 1)
        centered_interval(5.0, 1.0)
        """
        return "centered_interval({0}, {1})".format(float(self.center()), float(self.tolerance()))


###################
# Extra Questions #
###################

from operator import sub, mul

def make_anonymous_factorial():
    """Return the value of an expression that computes factorial.

    >>> make_anonymous_factorial()(5)
    120
    >>> from construct_check import check
    >>> check(HW_SOURCE_FILE, 'make_anonymous_factorial', ['Assign', 'AugAssign', 'FunctionDef', 'Recursion'])
    True
    """
    return lambda n: 1 if n == 1 else mul(n, make_anonymous_factorial()(n - 1))
