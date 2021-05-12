import math
from numpy import cross
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
        return f"{self.value:.2f}i"


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
        return f"{self.value:.2f}j"


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
        return f"{self.value:.2f}k"


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

    def __neg__(self):
        return VectorPart(-self.i.value, -self.j.value, -self.k.value)

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return VectorPart(self.i.value * other,
                              self.j.value * other,
                              self.k.value * other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return VectorPart(self.i.value / other,
                              self.j.value / other,
                              self.k.value / other)

    def __matmul__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError

        v_product = [vec1 * vec2 for vec1, vec2 in zip(self, other)]

        return reduce(lambda x, y: x + y, v_product)

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return VectorPart(self.i.value + other.i.value,
                              self.j.value + other.j.value,
                              self.k.value + other.k.value)

        elif isinstance(other, IVec):
            return VectorPart(self.i + other.value,
                              self.j.value,
                              self.k.value)

        elif isinstance(other, JVec):
            return VectorPart(self.i.value,
                              self.j.value + other.value,
                              self.k.value)

        elif isinstance(other, KVec):
            return VectorPart(self.i.value,
                              self.j.value,
                              self.k.value + other.value)

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

    def __iter__(self):
        yield self.scalar_part
        for part in self.vector_part:
            yield part

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(self.scalar_part * other, self.vector_part * other)

        if isinstance(other, self.__class__):
            a, b, c, d = self
            e, f, g, h = other

            # Derivation: https://www.youtube.com/watch?v=jlskQDR8-bY
            return Quaternion(
                (a * e) - self.vector_part @ other.vector_part,
                VectorPart(
                    (b * e) + (a * f) - (d * g) + (c * h),
                    (c * e) + (d * f) + (a * g) - (b * h),
                    (d * e) - (c * f) + (b * g) + (a * h)
                )
            )

    def __add__(self, other):
        if isinstance(other, (float, int)):
            return Quaternion(self.scalar_part + other, self.vector_part)
        if isinstance(other, self.__class__):
            return Quaternion(self.scalar_part + other.scalar_part,
                              self.vector_part + other.vector_part)

    def __neg__(self):
        return Quaternion(self.scalar_part, -self.vector_part)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return Quaternion(self.scalar_part / other, self.vector_part / other)

    def __repr__(self):
        return f"{self.scalar_part:.2f}, {self.vector_part}"

    def normalize(self):
        return self / math.sqrt(self @ self)


if __name__ == '__main__':

    angle = math.pi/2
    print("\nFull Test:")
    q1 = Quaternion(0, VectorPart(1, 0, 0)).normalize()
    q2 = -q1
    p = Quaternion(0, VectorPart(0, 0, 1))

    result = (q1 * math.sin(angle / 2) + math.cos(angle / 2)) \
             * p \
             * (q1 * math.sin(-angle / 2) + math.cos(-angle / 2))

    print(f"Rotating ( {p}) about ( {q1}) by {math.degrees(angle)} degrees:\n\t> ( {result})")
