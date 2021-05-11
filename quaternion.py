import math
from functools import reduce


class ImaginaryValue:
    def __init__(self, value: float):
        self.value = value

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.value + other.value)
        else:
            raise TypeError

    def __truediv__(self, other):
        if isinstance(other, (float, int)):
            return self.value / other

    def __sub__(self, other):
        return self.value - other.value

    def __neg__(self):
        return self.__class__(-self.value)

    def __float__(self):
        return self.value

    def __repr__(self):
        return str(self)

class IVec(ImaginaryValue):
    def __init__(self, value: float):
        super().__init__(value)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return IVec(self.value * other)

        if isinstance(other, IVec):
            return self.value * other.value * -1

        elif isinstance(other, JVec):
            return KVec(self.value * other.value)

        elif isinstance(other, KVec):
            return JVec(self.value * other.value * -1)

        else:
            raise TypeError

    def __str__(self):
        return f"{self.value:.3f}i"


class JVec(ImaginaryValue):
    def __init__(self, value: float):
        super().__init__(value)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return JVec(self.value * other)

        if isinstance(other, IVec):
            return KVec(self.value * other.value * -1)

        elif isinstance(other, JVec):
            return self.value * other.value * -1

        elif isinstance(other, KVec):
            return IVec(self.value * other.value)

        else:
            raise TypeError

    def __str__(self):
        return f"{self.value:.3f}j"



class KVec(ImaginaryValue):
    def __init__(self, value: float):
        super().__init__(value)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return KVec(self.value * other)

        if isinstance(other, IVec):
            return JVec(self.value * other.value)

        elif isinstance(other, JVec):
            return IVec(self.value * other.value * -1)

        elif isinstance(other, KVec):
            return self.value * other.value * -1

        else:
            raise TypeError

    def __str__(self):
        return f"{self.value:.3f}k"


class VectorPart:
    def __init__(self, i, j, k):
        self.i = IVec(i)
        self.j = JVec(j)
        self.k = KVec(k)

    def __iter__(self):
        yield self.i.value
        yield self.j.value
        yield self.k.value

    def __repr__(self):
        return f"{{ {self.i}, {self.j}, {self.k} }}"

    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError

        return VectorPart(self.i * other.i,
                          self.j * other.j,
                          self.k * other.k)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return VectorPart(self.i / other,
                              self.j / other,
                              self.k / other)

    def __matmul__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError

        v_product = []
        for vec1, vec2 in zip(self, other):
            v_product.append(vec1 * vec2)

        return reduce(lambda x, y: x + y, v_product)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return VectorPart(self.i + other.i,
                              self.j + other.j,
                              self.k + other.k)

        elif isinstance(other, IVec):
            return VectorPart(self.i + other.value,
                              self.j,
                              self.k)

        elif isinstance(other, JVec):
            return VectorPart(self.i,
                              self.j + other.value,
                              self.k)

        elif isinstance(other, KVec):
            return VectorPart(self.i,
                              self.j,
                              self.k + other.value)

        else:
            raise TypeError


class Quaternion:
    def __init__(self, scalar_part: float, vector_part: VectorPart):
        self.scalar_part = scalar_part
        self.vector_part = vector_part

    def __matmul__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError

        return (self.vector_part @ other.vector_part) + self.scalar_part * other.scalar_part

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(self.scalar_part / other, self.vector_part / other)

    def __repr__(self):
        return f"{self.scalar_part:.3f}, {self.vector_part}"

    def normalize(self):
        return self / math.sqrt(self @ self)


if __name__ == '__main__':
    v1 = IVec(3)
    v2 = JVec(3)
    v3 = KVec(3)

    print("IVec Tests:")
    print(v1 * 3.1)
    print(v1 * v1)
    print(v1 * v2)
    print(v1 * v3)

    print("\nJVec Tests:")
    print(v2 * 3.1)
    print(v2 * v1)
    print(v2 * v2)
    print(v2 * v3)

    print("\nKVec Tests:")
    print(v3 * 3.1)
    print(v3 * v1)
    print(v3 * v2)
    print(v3 * v3)

    print("\nUnary Tests:")
    print(-v1)

    print("\nBinary Tests:")
    vector_part1 = VectorPart(1, 3, -5)
    vector_part2 = VectorPart(4, -2, -1)

    print(f"Addition: {v1 + v1}")
    print(f"Subtraction: {v1 - v1}")
    print(f"Product: {vector_part1 * vector_part2}")
    print(f"Dot Product: {vector_part1 @ vector_part2}")

    q1 = Quaternion(3, vector_part1)
    print(q1)
    print(q1.normalize())
