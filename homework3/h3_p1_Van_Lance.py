
from ast import main
# Lance Van Z23504457

class NVector:
    #a, b
    def __init__(self, *args):
        """Initializes a vector from a sequence or multiple numbers."""
        if len(args) == 1:
            self.elements = list(args[0])
        else:
            self.elements = list(args)

    # c
    def __len__(self):
        """Returns the number of elements in the vector."""
        return len(self.elements)

    # d
    def __getitem__(self, index):
        """Returns the element at the index."""
        return self.elements[index]

    # e
    def __setitem__(self, index, value):
        """Assigns a value to the element at the index."""
        self.elements[index] = value

    # f
    def __str__(self):
        """Returns a readable string representation of the vector."""
        return f"NVector({self.elements})"

    # g
    def __eq__(self, other):
        """Returns True if both vectors have equal elements."""
        if not isinstance(other, NVector):
            return False
        return self.elements == other.elements

    def __ne__(self, other):
        """Returns True if the vectors are not equal."""
        return not self.__eq__(other)
    
    # h
    def __add__(self, other):
        """Add a number or another vector element-wise."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have the same length")
            return NVector([a + b for a, b in zip(self.elements, other.elements)])

        if isinstance(other, (int, float)):
            return NVector([a + other for a in self.elements])

        return NotImplemented

    def __radd__(self, other):
        """Supports addition with a number on the left."""
        return self.__add__(other)

    # i
    def __mul__(self, other):
        """Multiplys by a scalar or compute the dot product."""
        if isinstance(other, NVector):
            if len(self) != len(other):
                raise ValueError("Vectors must have the same length")
            return sum(a * b for a, b in zip(self.elements, other.elements))

        if isinstance(other, (int, float)):
            return NVector([a * other for a in self.elements])

        return NotImplemented

    def __rmul__(self, other):
        """Supports multiplication with a number on the left."""
        return self.__mul__(other)

    # j
    @classmethod
    def zeros(cls, n):
        """Returns a new vector containing n zeros."""
        if not isinstance(n, int):
            raise TypeError("Dimension must be an integer")
        if n < 0:
            raise ValueError("Dimension cannot be negative")
        return cls([0] * n)

def main():
    v = NVector(3, 0, 1, -1)

    print(v)
    print(len(v))
    print(v[1])
    print(v + 10)
    print(v * 2)
    print(NVector.zeros(4))

if __name__ == "__main__":
    main()