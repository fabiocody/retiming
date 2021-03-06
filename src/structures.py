#!/usr/bin/env python3


class MyTuple(tuple):
    """
    This class is used in *Algorithm WD* in order to implement custom sum and comparison.
    """

    def __add__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return MyTuple(x+other for x in self)
        elif isinstance(other, tuple) and len(self) == len(other):
            return MyTuple(x + y for x, y in zip(self, other))
        else:
            raise NotImplementedError()

    def __radd__(self, other):
        return self.__add__(other)

    def __compare__(self, other):
        assert isinstance(other, tuple) and len(self) == len(other)
        for i in range(len(self)):
            diff = self[i] - other[i]
            if diff != 0:
                return diff
        return 0

    def __lt__(self, other):
        if isinstance(other, tuple) and len(self) == len(other):
            return self.__compare__(other) < 0
        elif isinstance(other, int) or isinstance(other, float):
            for i in range(len(self)):
                if self[i] >= other:
                    return False
            return True
        else:
            return False

    def __gt__(self, other):
        if isinstance(other, tuple) and len(self) == len(other):
            return self.__compare__(other) > 0
        elif isinstance(other, int) or isinstance(other, float):
            for i in range(len(self)):
                if self[i] <= other:
                    return False
            return True
        else:
            return False

    def __le__(self, other):
        if isinstance(other, tuple) and len(self) == len(other):
            return self.__compare__(other) <= 0
        elif isinstance(other, int) or isinstance(other, float):
            for i in range(len(self)):
                if self[i] > other:
                    return False
            return True
        else:
            return False

    def __ge__(self, other):
        if isinstance(other, tuple) and len(self) == len(other):
            return self.__compare__(other) >= 0
        elif isinstance(other, int) or isinstance(other, float):
            for i in range(len(self)):
                if self[i] < other:
                    return False
            return True
        else:
            return False

    def __eq__(self, other):
        if isinstance(other, tuple):
            if len(self) == len(other):
                return self.__compare__(other) == 0
        return False
