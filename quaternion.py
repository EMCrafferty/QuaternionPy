class ImaginaryValue:
    def __init__(self, value: float):
        self.value = value

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self.__class__(self.value + other.value)
        else:
            raise TypeError

    def __neg__(self):
        return self.__class__(-self.value)


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
        return f"{self.value}i"


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
        return f"{self.value}j"


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
        return f"{self.value}k"


class VectorPart:
    def __init__(self, i: IVec, j: JVec, k: KVec):
        self.i = i
        self.j = j
        self.k = k


class Quaternion:
    scalar_part: float
    i: IVec


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
