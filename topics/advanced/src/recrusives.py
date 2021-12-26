def factorial(n: int = 0):
    """Factorial is a mathematics function based on a non-negative interger n, denoted of n!
    It has calculated by the product of all positive intergers less than or equal n.
    Symponis:
        n! = n.(n-1).(n-2).....3.2.1
    Examples:
        4! = 4.3.2.1 = 24
    
    Args:
        n [int]: the interger pre-defined to be factorial.

    Returns:
        [int]: factorial of n

    Referrences:
    [1] [Factorial from Wiki](https://en.wikipedia.org/wiki/Factorial)
    """
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)


def fib(n: int = 0):
    """Fibonacci function to create fibonacci numbers
    Version: recursive version
    
    Args:
        n [int]: the position of fibonacci number in fibonacci array, start with 0

    Returns:
        [int]: return number that in position n
    """
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def fibi(n):
    """Fibonacci function in interactive mode"""
    old, new = 0, 1
    if n == 0:
        return 0
    for i in range(n-1):
        old, new = new, old + new
    return new


memo = {0:0, 1:1}
def fibm(n: int = 0):
    """Fibonacci function with support of memory"""
    if not n in memo:
        memo[n] = fibm(n-1) + fibm(n-2)
    return memo[n]


def muln(n: int, m: int):
    """Multiple of m with n

    Args:
        n (int): position
        m (int): multiple

    Returns:
        (int): number that recursive multiple of m

    Examples: 
    > muln(100, 4)
    > muln(3, 3)
    """
    if n == 1:
        return m
    else:
        return m * muln(n - 1, m)


def recursive_sum(n: int):
    """Recursive sum is a function sum along to non-negative interger n
    Symponis:
        sum(n) = n + (n-1) + (n-2)+...+ 3 + 2 + 1 + 0
    Examples:
        sum(4) = 4 + 3 + 2 + 1 = 10
    
    Args:
        n [int]: the interger pre-defined

    Returns:
        [int]: the sum of the first n integers.
    """
    if n == 0:
        return 0
    else:
        return n + recursive_sum(n-1)


class kFibonacci:
    """
    Read more at: Generalized Fibonacci Sequence of [Recursive function](https://python-course.eu/advanced-python/recursive-functions.php)
    """

    def __init__(self, k, initials, cofficients):
        self.memo = dict(zip(range(k), initials))
        self.coeffs = cofficients
        self.k = k

    def __call__(self, n):
        k = self.k
        if n not in self.memo:
            result = 0
            for coeff, i in zip(self.coeffs, range(1, k+1)):
                print(coeff, i)
                result += coeff * self.__call__(n-i)
            self.memo[n] = result
        return self.memo[n]
