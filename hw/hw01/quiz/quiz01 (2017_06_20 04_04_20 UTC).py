def multiple(a, b):
    """Return the smallest number n that is a multiple of both a and b.

    >>> multiple(3, 4)
    12
    >>> multiple(14, 21)
    42
    """
    def gcf(num1,num2):
        factor = 1
        if num1 == num2:
            return num1
        elif num1 > num2:
            for x in range(1, num2):
                if num2 % x == 0:
                    factor = x
            return factor
        else:
            for x in range(1, num1):
                if num1 % x == 0:
                    factor = x
            return factor

    return a*b // gcf(a,b)



def unique_digits(n):
    """Return the number of unique digits in positive integer n

    >>> unique_digits(8675309) # All are unique
    7
    >>> unique_digits(1313131) # 1 and 3
    2
    >>> unique_digits(13173131) # 1, 3, and 7
    3
    >>> unique_digits(10000) # 0 and 1
    2
    >>> unique_digits(101) # 0 and 1
    2
    >>> unique_digits(10) # 0 and 1
    2
    """
    def has_digit(digit,number):
        while number > 0:
            if number % 10 == digit:
                return True
            number = number // 10

    digits = 0
    for x in range(0, 10):
        if has_digit(x,n):
            digits += 1
    return digits
