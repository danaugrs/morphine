# Python modules
from itertools import combinations, product
from collections import Counter


class Polynomial:
    def __init__(self, *args):
        self.values = Counter(args)

    def __iter__(self):
        return iter(self.elements())

    def __getitem__(self, key):
        return self.elements()[key]

    def __str__(self):
        return type(self).__name__+str(self.elements())#sorted(self.values))

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash(type(self).__name__) + hash(tuple(self.elements()))

    def __lt__(self, other):
        if isinstance(other, int):
            return False
        if isinstance(other, Polynomial):
            if type(self).__name__ == type(other).__name__:
                if len(self.values.keys()) < len(other.values.keys()):
                    return True
                return False
            return len(type(self).__name__) < len(type(other).__name__)

    def __gt__(self, other):
        return not self.__lt__(other)

    def __eq__(self, other):
        return hash(flatten(self)) == hash(flatten(other))

    def __ne__(self, other):
        return hash(self) != hash(other)

    def elements(self):
        return sorted(self.values.elements())

    def eval(self, values):
        return evaluate(values, self)

class Sum(Polynomial):
    pass

class Prod(Polynomial):
    pass


def evaluate(values: list, polynomial: Polynomial):
    """Evaluate a polynomial using the provided values."""
    pt = type(polynomial)  
    if pt == Sum:
        return sum(evaluate(values, i) for i in polynomial)
    elif pt == Prod:
        res = 1
        for item in polynomial:
            res *= evaluate(values, item)
        return res
    else:
        return values[polynomial]


def elementary_symmetric(size: int, degree: int):
    """Return the elementary symmetric polynomial of specified size and degree."""
    c = list(combinations(range(size), degree))
    products = [Prod(*i) if len(i) > 1 else i[0] for i in c]
    return Sum(*products) if len(products) > 1 else products[0]


def normalize(poly: Polynomial):
    """Unroll equivalent nested operations."""
    pt = type(poly)
    if issubclass(pt, Polynomial):
        if len(poly.elements()) == 1:
            return normalize(poly[0])
        new_elements = []
        for p in poly:
            if type(p) == pt:
                v = normalize(p)
                new_elements.extend(v)
            else:
                new_elements.append(normalize(p))
        return pt(*new_elements)
    else:
        return poly


def flatten(polynomial: Polynomial, parent=None):
    """Flatten a polynomial to the minimal depth."""
    normalized = normalize(polynomial)
    def _flatten(polynomial: Polynomial):
        # TODO; recursive
        # print('flattening', polynomial)

        # is_sum = type(polynomial) == Sum
        # is_prod = type(polynomial) == Prod

        return polynomial

    return _flatten(normalized)


if __name__ == '__main__':

    assert Sum(1, 2) == Sum(1, 2)
    assert Sum(1, 1) != Sum(1)
    assert Sum(1, 2) == Sum(2, 1)
    assert Sum(1, 2) != frozenset([1, 2])
    assert Sum(1, 2) != Sum(1, 3)
    assert Prod(3, 6) == Prod(6, 3)
    assert Sum(10, 20) != Prod(10, 20)
    assert Sum(3, 2, Prod(21, 4)) == Sum(Prod(4, 21), 3, 2)

    assert hash(Sum(1, 2)) == hash(Sum(1, 2))
    assert hash(Sum(1, 1)) != hash(Sum(1))
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

    # TODO test ordering of nested polynomials - len(poly) should also take into account the items' length
    
    assert normalize(Sum(Sum(0, Sum(1, 2)), Sum(0, 1))) == Sum(0, 0, 1, 1, 2)
    assert normalize(Sum(Sum(0, 1), Sum(0, 1, 3, 1))) == Sum(0, 0, 1, 1, 1, 3)
    assert normalize(Prod(Prod(0, 1), Prod(0, 1))) == Prod(0, 0, 1, 1)
    assert normalize(Prod(Sum(3), Prod(Sum(1, 2), 5, 0, 4))) == Prod(0, 3, 4, 5, Sum(1, 2))
    assert normalize(Prod(Sum(0, Prod(1, 2)), Sum(0, 1))) == Prod(Sum(0, Prod(1, 2)), Sum(0, 1))
    
    assert Sum(Prod(1)) == Sum(1)
    assert Sum(Prod(Sum(1))) == Prod(1)

    nested = Prod(Sum(0, Prod(1, 2)), Sum(0, 1))

    assert normalize(nested) == nested

    #TODO implement flatten()
    print(flatten(nested))
    # assert flatten(nested) == Sum(Prod(0, 0), Prod(0, 1), Prod(0, 1, 2), Prod(1, 1, 2))
    
    # print(flatten(flatten(flatten(Prod(Sum(0, Prod(1, 2)), Sum(0, 1))))))
    # print(flatten(flatten(flatten(flatten(Prod(Sum(0, Prod(1, 2)), Sum(0, 1)))))))
    # assert flatten(Prod(0, Sum(0,1))) == Sum(Prod(0, 0), Prod(0, 1))
    # assert flatten(Sum(Sum(0, Sum(1, 2)), Sum(0, 1))) == Sum(0, 0, 1, 1, 2)
    # assert flatten(Prod(Sum(0, Prod(1, 2)), Sum(0, 1))) == Sum(Prod(0, 0), Prod(0, 1), Prod(0, 1, 2), Prod(1, 1, 2))
    # assert flatten(Prod(2, Sum(0, 1))) == Sum(Prod(0, 2), Prod(1, 2))
 