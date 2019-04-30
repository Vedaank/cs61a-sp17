def twenty_seventeen():
    """Come up with the most creative expression that evaluates to 2017,
    using only numbers and the +, *, and - operators.

    >>> twenty_seventeen()
    2017
    """
    val = 1
    for x in range(0,64):
        val += x
    return val
