##################################
# Newton's method (from lecture) #
##################################

def improve(update, close, guess=1, max_updates=100):
    """Iteratively improve guess with update until close(guess) is true."""
    k = 0
    while not close(guess) and k < max_updates:
        guess = update(guess)
        k = k + 1
    return guess

def approx_eq(x, y, tolerance=1e-15):
    """Whether x is within tolerance of y."""
    return abs(x - y) < tolerance

def find_zero(f, df):
    """Return a zero of the function f with derivative df."""
    def near_zero(x):
        return approx_eq(f(x), 0)
    return improve(newton_update(f, df), near_zero)

def newton_update(f, df):
    """Return an update function for f with derivative df."""
    def update(x):
        return x - f(x) / df(x)
    return update

def nth_root_of_a(n, a):
    """Return the nth root of a.

    >>> nth_root_of_a(2, 64)
    8.0
    >>> nth_root_of_a(3, 64)
    4.0
    >>> nth_root_of_a(6, 64)
    2.0
    """
    return find_zero(lambda x: pow(x, n) - a, lambda x: n * pow(x, n-1))

#############
# Questions #
#############

def intersect(f, df, g, dg):
    """Return where f with derivative df intersects g with derivative dg.

    >>> parabola, line = lambda x: x*x - 2, lambda x: x + 10
    >>> dp, dl = lambda x: 2*x, lambda x: 1
    >>> intersect(parabola, dp, line, dl)
    4.0
    """
    return find_zero(lambda x: f(x) - g(x), lambda x: df(x) - dg(x))

# Huffman encoding trees

def huffman_leaf(letter, weight):
    """A leaf of a Huffman tree, which has a weight at the root."""
    return tree(weight, [tree(letter)])

def huffman_tree(left, right):
    """A Huffman encoding tree; left and right are also Huffman trees."""
    return tree(label(left) + label(right), [left, right])

def weight(tree):
    """The weight of a Huffman encoding tree."""
    return label(tree)

def is_huffman_leaf(tree):
    """Whether this Huffman tree is a Huffman leaf."""
    return not is_leaf(tree) and is_leaf(branches(tree)[0])

def letter(leaf):
    """The letter of a Huffman leaf."""
    return label(branches(leaf)[0])

# Trees (from lecture)
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

CD = huffman_tree(huffman_leaf('c', 1), huffman_leaf('d', 1))
EF = huffman_tree(huffman_leaf('e', 1), huffman_leaf('f', 1))
GH = huffman_tree(huffman_leaf('g', 1), huffman_leaf('h', 1))
EFGH = huffman_tree(EF, GH)
BCD = huffman_tree(huffman_leaf('b', 3), CD)
BCDEFGH = huffman_tree(BCD, EFGH)
example_tree = huffman_tree(huffman_leaf('a', 8), BCDEFGH)

def letters(tree):
    """Return a list of all letters encoded in Huffman encoding TREE.

    >>> letters(example_tree)
    ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    """
    def helper(tree):
        if is_huffman_leaf(tree):
            return letter(tree)
        else:
            return [letters(l) for l in branches(tree)]
    all_letters = []
    for item in helper(tree):
        if item is list:
            for elem in item:
                all_letters += elem
        else:
            all_letters += item
    return all_letters

def decode(tree, code):
    """Decode CODE, a list of 0's and 1's using the Huffman encoding TREE.

    >>> decode(example_tree, [1, 0, 0, 0, 1, 1, 1, 1])
    'bah'
    """
    word = ''
    while code:
        word += decode_one(tree, code)
    return word

def decode_one(tree, code):
    """Decode and remove the first letter in CODE, using TREE.

    >>> code = [1, 0, 0, 0, 1, 1, 1, 1]
    >>> decode_one(example_tree, code)
    'b'
    >>> code # The initial 1, 0, and 0 are removed by decode_one
    [0, 1, 1, 1, 1]
    """
    if is_huffman_leaf(tree):
        return letter(tree)
    else:
        return decode_one(branches(tree)[code.pop(0)], code)

def encodings(tree):
    """Return all encodings in a TREE as a dictionary that maps symbols to
    bit lists.

    >>> e = encodings(example_tree)
    >>> set(e.keys()) == set('abcdefgh')
    True
    >>> e['a']
    [0]
    >>> e['c']
    [1, 0, 1, 0]
    >>> e['h']
    [1, 1, 1, 1]
    """
    answer = ""
    for branches in tree:
        co = find(lambda p: p.name == s, code)
        if ( not co  ):
            import sys
            print >> sys.stderr, "Warning: symbol",`s`,"has no encoding!"
            pass
        else:
            answer = answer + co.word
            pass
    return answer
 


def huffman(frequencies):
    """Return a Huffman encoding for FREQUENCIES, a list of (symbol,
    frequency) pairs.

    >>> frequencies = [('a', 8), ('b', 3), ('c', 1), ('d', 1)]
    >>> h = huffman(frequencies)
    >>> for letter, code in sorted(encodings(h).items()):
    ...     print(letter + ':', code)
    a: [1]
    b: [0, 1]
    c: [0, 0, 0]
    d: [0, 0, 1]
    """
    frequencies.sort(key=lambda freq: freq[1]) # lowest frequencies first
    leaves = [huffman_leaf(letter, freq) for letter, freq in frequencies]
    

def huffman_wiki():
    """Return a Huffman encoding tree for the text of the Huffman coding page
    on Wikipedia. (Internet connection required!)

    Note: Sometimes encodings are slightly different than the ones in the test,
          depending on the content returned by Wikipedia.

    >>> e = encodings(huffman_wiki())
    >>> [[letter, e[letter]] for letter in ['a', 'b', 'c']]
    [['a', [0, 0, 1, 0]], ['b', [1, 0, 0, 0, 1, 0]], ['c', [0, 1, 0, 1, 1]]]
    """
    from urllib.request import urlopen
    from json import loads
    from collections import Counter
    huff = urlopen('http://goo.gl/w1Jdjj').read().decode()
    content = loads(huff)['query']['pages']['13883']['revisions'][0]['*']
    return huffman(list(Counter(content).items()))

from operator import *

def make_ternary_constraint(a, b, c, ab, ca, cb):
    """The constraint that ab(a,b)=c and ca(c,a)=b and cb(c,b) = a."""
    def new_value():
        av, bv, cv = [connector['has_val']() for connector in (a, b, c)]
        if av and bv:
            c['set_val'](constraint, ab(a['val'], b['val']))
        elif av and cv:
            b['set_val'](constraint, ca(c['val'], a['val']))
        elif bv and cv:
            a['set_val'](constraint, cb(c['val'], b['val']))
    def forget_value():
        for connector in (a, b, c):
            connector['forget'](constraint)
    constraint = {'new_val': new_value, 'forget': forget_value}
    for connector in (a, b, c):
        connector['connect'](constraint)
    return constraint

def adder(a, b, c):
    """The constraint that a + b = c."""
    return make_ternary_constraint(a, b, c, add, sub, sub)

def multiplier(a, b, c):
    """The constraint that a * b = c."""
    return make_ternary_constraint(a, b, c, mul, truediv, truediv)

def constant(connector, value):
    """The constraint that connector = value."""
    constraint = {}
    connector['set_val'](constraint, value)
    return constraint

def connector(name=None):
    """A connector between constraints."""
    informant = None
    constraints = []
    def set_value(source, value):
        nonlocal informant
        val = connector['val']
        if val is None:
            informant, connector['val'] = source, value
            if name is not None:
                print(name, '=', value)
            inform_all_except(source, 'new_val', constraints)
        else:
            if val != value:
                print('Contradiction detected:', val, 'vs', value)
    def forget_value(source):
        nonlocal informant
        if informant == source:
            informant, connector['val'] = None, None
            if name is not None:
                print(name, 'is forgotten')
            inform_all_except(source, 'forget', constraints)
    connector = {'val': None,
                 'set_val': set_value,
                 'forget': forget_value,
                 'has_val': lambda: connector['val'] is not None,
                 'connect': lambda source: constraints.append(source)}
    return connector

def inform_all_except(source, message, constraints):
    """Inform all constraints of the message, except source."""
    for c in constraints:
        if c != source:
            c[message]()

def squarer(a, b):
    """The constraint that a*a=b.

    >>> x, y = connector('X'), connector('Y')
    >>> s = squarer(x, y)
    >>> x['set_val']('user', 10)
    X = 10
    Y = 100
    >>> x['forget']('user')
    X is forgotten
    Y is forgotten
    >>> y['set_val']('user', 16)
    Y = 16
    X = 4.0
    """
    def new_value():
        if a['set_val']():
            b['set_val'](constraint, a['val'] ** 2)
        elif b['has_val']():
            a['set_val'](constraint, b['val'] ** 0.5)

    def forget_value():
        a['forget'](constraint)
        b['forget'](constraint)
    
    constraint = {'new_val': new_value, 'forget': forget_value}
    a['connect'](constraint)
    b['connect'](constraint)

    return constraint

def pythagorean(a, b, c):
    """Connect a, b, and c into a network for the Pythagorean theorem:
    a*a + b*b = c*c

    >>> a, b, c = [connector(name) for name in ('A', 'B', 'C')]
    >>> pythagorean(a, b, c)
    >>> a['set_val']('user', 5)
    A = 5
    >>> c['set_val']('user', 13)
    C = 13
    B = 12.0
    """
    asquared, bsquared, csquared = [connector() for _ in  range(3)]
    squarer(a, asquared)
    squarer(b, bsquared)
    squarer(c, csquared)
    adder(asquared, bsquared, csquared)
    


#########

# Extra #
#########

## Lambda calculus.

# Every lambda-calculus expression is a Term, a class with the following
# subtypes:

#    Sym('x') represents the symbol x.
#    Lambda(s, t), where s is a Sym and t is an arbitrary Term, represents
#        the lambda term
#           \ s. t
#        (where \ denotes lambda here).
#    Apply(e1, e2), where e1 and e2 are Terms, represents the application
#    (e1 e2).

# Thus, the lambda expression
#    \ x. \ y. y x y
# could be represented by E, where
#    x = Sym('x')
#    y = Sym('y')
#    E = Lambda(x, Lambda(y, Apply(Apply(y, x), y)))
#

class Term:
    """The supertype of all terms in the lambda calculus."""

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self._str(True, True)

    def isFree(self, var):
        """True iff VAR appears free (not lambda bound) in SELF."""
        raise NotImplementedError

    def beta(self):
        """Attempt to find a beta reduction in SELF. If found, return
        (S', True), where S' is the result of applying the reduction.  Otherwise
        return (SELF, False)."""
        raise NotImplementedError

    def subst(self, var, val):
        """The result of substituting VAL for all free occurrences of VAR in SELF."""
        raise NotImplementedError

class Prim(Term):
    """A primitive combinator."""

    def __init__(self, id, arity, redux):
        """The combinator denoted by ID, and performing the reduction REDUX
        when applied to ARITY arguments."""
        self._id, self._arity, self._redux = id, arity, redux

    def _str(self, leftd, rightd):
        return self._id

    def isFree(self, var):
        return False

    def beta(self):
        return self, False

    def subst(self, var, val):
        return self

    def arity(self):
        return self._arity

    def redux(self, args):
        return self._redux(*args)

class Sym(Term):
    """A symbol."""

    uid = 0

    def __init__(self, id):
        """The symbol whose printed form is ID."""
        self._id = id

    def _str(self, leftd, rightd):
        return self._id

    def __eq__(self, other):
        if type(other) is Sym:
            return other._id == self._id
        else:
            return False

    def isFree(self, var):
        return self == var

    def beta(self):
        return self, False

    def subst(self, var, val):
        if var == self:
            return val
        else:
            return self

    @staticmethod
    def new_var():
        Sym.uid += 1
        return Sym('v' + str(Sym.uid))

class Apply(Term):
    """An application term."""

    def __init__(self, left, right):
        """The application (LEFT RIGHT)."""
        if type(left) is list or type(right) is list:
            print("?", left, right)
        self._left, self._right = left, right

    def _str(self, leftd, rightd):
        if not leftd:
            return "({} {})".format(self._left._str(True, False),
                                    self._right._str(False, True))
        else:
            return "{} {}".format(self._left._str(True, False),
                                  self._right._str(False, rightd))

    def isFree(self, var):
        return self._left.isFree(var) or self._right.isFree(var)

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._right

    def _getPrim(self, nesting):
        p = self
        if type(self._left) is Prim:
            if nesting + 1 == self._left.arity():
                return self._left, [self._right]
        elif type(self._left) is Apply:
            prim, args = self._left._getPrim(nesting + 1)
            if prim:
                return prim, args + [self._right]
        return None, None

    def beta(self):
        if type(self._left) is Lambda:
            return self._left.apply(self._right), True
        prim, args = self._getPrim(0)
        if prim:
            return prim.redux(args), True
        else:
            left, change = self._left.beta()
            if change:
                return Apply(left, self._right), True
            right, change = self._right.beta()
            if change:
                return Apply(left, right), True
            return self, False

    def subst(self, var, val):
        return Apply(self._left.subst(var, val), self._right.subst(var, val))

class Lambda(Term):
    """A lambda term."""

    def __init__(self, var, body):
        """The term \ VAR. BODY."""
        self._var, self._body = var, body

    def _str(self, leftd, rightd):
        if rightd:
            return "\\{}. {}".format(self._var, self._body._str(True, True))
        else:
            return "(\\{}. {})".format(self._var, self._body._str(True, True))
    def isFree(self, var):
        return var != self._var and self._body.isFree(var)

    def beta(self):
        return self, False

    def apply(self, arg):
        return self._body.subst(self._var, arg)

    def subst(self, var, val):
        if var == self._var:
            return self
        elif val.isFree(self._var):
            newv = Sym.new_var()
            new_body = self._body.subst(self._var, newv).subst(var, val)
            return Lambda(newv, new_body)
        return Lambda(self._var, self._body.subst(var, val))

# Shorthand for some symbols.

x = Sym('x')
y = Sym('y')
z = Sym('z')
a = Sym('a')
b = Sym('b')
f = Sym('f')
n = Sym('n')
p = Sym('p')

LM = "LAMBDA"

def lexpr(E):
    r"""A convenience method for writing terms:
    >>> lexpr([x, y, [y, y], z])
    x y (y y) z
    >>> lexpr([LM, x, x, y])
    \x. x y
    """
    if type(E) is list or type(E) is tuple:
        if E[0] == LM:
            result = Lambda(E[1], lexpr(E[2:]))
        else:
            result = lexpr(E[0])
            for k in range(1, len(E)):
                term = E[k]
                if term == LM:
                    result = Apply(result, Lambda(E[k+1], lexpr(E[k+2:])))
                    break
                result = Apply(result, lexpr(term))
    else:
        result = E
    return result


def reduce(term, lim=10):
    r"""Apply beta reductions to TERM up to LIM times, or until TERM contains no
    further reductions.
    >>> reduce(Apply(Lambda(y, y), x))
    x
    >>> reduce(Apply(Lambda(x, y), z))
    y
    >>> reduce(Apply(x, z))
    x z
    >>> E = Lambda(x, Lambda(y, Apply(y, x)))
    >>> E
    \x. \y. y x
    >>> reduce(Apply(E, z))
    \y. y z
    """

    changed = True
    while lim > 0 and changed:
        term, changed = term.beta()
        lim -= 1
    return term

# Logic and conditionals

# These two are in long-hand:
TRUE       = Lambda(x, Lambda(y, x))
FALSE      = Lambda(x, Lambda(y, y))
# The rest use lexpr:
IFTHENELSE = lexpr([LM, p, LM, x, LM, y,   p, x, y])   # \p. \x. \y. p x y
AND        = lexpr([LM, x, LM, y,   x, y, x])          # \x. \y. x y x
OR         = lexpr([LM, x, LM, y,   x, x, y])          # \x. \y. x x y
NOT        = lexpr([LM, x,   x, FALSE, TRUE])          # \x. x FALSE TRUE
ISZERO     = lexpr([LM, n,   n, [LM, y, FALSE], TRUE]) # \n. n (\y. FALSE) TRUE

# Pairs and Church numerals

# ID x => x
ID         = lexpr([LM, x, x])
ZERO       = lexpr([LM, f, LM, x,  x])
SUCCESSOR  = lexpr([LM, n, LM, f, LM, x, f, [n, f, x]])
ADD        = lexpr([LM, a, LM, b,  a, SUCCESSOR, b])
MULT       = lexpr([LM, a, LM, b,  a, [ADD, b], ZERO])

# (PAIR x y) TRUE => x;  (PAIR x y) FALSE => y
PAIR = None   # REPLACE WITH PAIR = lexpr(_________)

# The predecessor (-1) function for Church numerals.  First, you must get
# PAIR working.
PRED       = lexpr([LM, n, LM, f, LM, x,
                    n, [LM, p,  PAIR, f, [p, TRUE, [p, FALSE]]],
                    [PAIR, ID, x],
                    FALSE])

def testpair():
    r"""
    >>> reduce(lexpr([PAIR, x, y, TRUE]))
    x
    >>> reduce(lexpr([PAIR, x, y, FALSE]))
    y
    >>> reduce(lexpr([PRED, [SUCCESSOR, [SUCCESSOR, [SUCCESSOR, ZERO]]], f, x]),
    ...              lim=500)
    f (f x)
    """
    pass

fact = None # REPLACE WITH fact = lexpr(________)

def testfact():
    r"""
    >>> THREE = lexpr([SUCCESSOR, [SUCCESSOR, [SUCCESSOR, ZERO]]])
    >>> reduce(lexpr([fact, THREE, f, x]), 5000)
    f (f (f (f (f (f x)))))
    """
    pass