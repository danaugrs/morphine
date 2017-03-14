# Python modules
from itertools import combinations


class Polynomial:
    def __init__(self, *args):
        self.values = frozenset(args)

    def __iter__(self):
        return iter(self.values)

    def __str__(self):
        return type(self).__name__+str(set(self.values))#sorted(self.values))

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(type(self).__name__) + hash(self.values)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return hash(self) != hash(other)

    def eval(self, values):
        return evaluate(values, self)

class Sum(Polynomial):
    pass

class Prod(Polynomial):
    pass


def evaluate(values: list, polynomial: Polynomial):
    """Evaluate a polynomial using the provided values."""    
    if type(polynomial) == Sum:
        res = 0
        for item in polynomial:
            res += evaluate(values, item)
    elif type(polynomial) == Prod:
        res = 1
        for item in polynomial:
            res *= evaluate(values, item)
    else:
        res = values[polynomial]
    return res


def elementary_symmetric(size: int, degree: int):
    """Return the elementary symmetric polynomial of specified size and degree."""
    c = list(combinations(range(size), degree))
    products = [Prod(*i) if len(i) > 1 else i[0] for i in c]
    return Sum(*products) if len(products) > 1 else products[0]


def flatten(polynomial: Polynomial):
    """Flatten a polynomial to either (1) a sum of products (2) a sum (3) a product."""
    # TODO
    return polynomial


if __name__ == '__main__':

    assert Sum(1, 2) == Sum(1, 2)
    assert Sum(1, 2) == Sum(2, 1)
    assert Sum(1, 2) != frozenset([1, 2])
    assert Sum(1, 2) != Sum(1, 3)
    assert Prod(3, 6) == Prod(6, 3)
    assert Sum(10, 20) != Prod(10, 20)
    assert Sum(3, 2, Prod(21, 4)) == Sum(Prod(4, 21), 3, 2)

    assert hash(Sum(1, 2)) == hash(Sum(1, 2))
    assert hash(Sum(1, 2)) == hash(Sum(2, 1))
    assert hash(Sum(1, 2)) != hash(frozenset([1, 2]))
    assert hash(Sum(1, 2)) != hash(Sum(1, 3))
    assert hash(Prod(3, 6)) == hash(Prod(6, 3))
    assert hash(Sum(10, 20)) != hash(Prod(10, 20))
    assert hash(Sum(3, 2, Prod(21, 4))) == hash(Sum(Prod(4, 21), 3, 2))
    
    assert evaluate([10, 20, 30, 40], Sum(Prod(0, 1), Prod(2, 3))) == 1400
    assert evaluate([10, 20, 30, 40], Sum(Prod(0, 1, 2), Prod(3))) == 6040
    assert evaluate([1, 2, 3], Sum(Prod(Sum(0, 1), 2), Sum(0, 1), Prod(2), 0)) == 16
    assert Sum(Prod(Sum(0, 1), 2), Sum(0, 1), Prod(2), 0).eval([1, 2, 3]) == 16

    assert elementary_symmetric(4, 1) == Sum(0, 1, 2, 3)
    assert elementary_symmetric(4, 2) == Sum(Prod(0, 1), Prod(0, 2), Prod(0, 3), Prod(1, 2), Prod(1, 3), Prod(2, 3))
    assert elementary_symmetric(4, 3) == Sum(Prod(0, 1, 2), Prod(0, 1, 3), Prod(0, 2, 3), Prod(1, 2, 3))
    assert elementary_symmetric(4, 4) == Prod(0, 1, 2, 3)

    # TODO flatten
    # print(flatten(Prod(Sum(0, Prod(1, 2)), Sum(0, 1))))
    # assert flatten(Prod(Sum(0, Prod(1, 2)), Sum(0, 1))) == Sum(Prod(0, 0), Prod(0, 1), Prod(0, 1, 2), Prod(1, 1, 2))

    # TODO make these the same ( maybe just call flatten() inside Polynomial.__hash__() )
    # assert Sum(Prod(1)) == Sum(1)
    # assert Sum(Prod(1)) == Prod(1)
