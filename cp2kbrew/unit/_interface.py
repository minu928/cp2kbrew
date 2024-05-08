from abc import ABCMeta, abstractmethod


class UnitConvertInterface(metaclass=ABCMeta):
    def __add__(self, other):
        return self.value + float(other)

    def __sub__(self, other):
        return self.value - float(other)

    def __mul__(self, other):
        return self.value * float(other)

    def __truediv__(self, other):
        return self.value / float(other)

    def __pow__(self, other):
        return self.value**other

    def __float__(self) -> float:
        return float(self.value)

    def __repr__(self) -> str:
        return str(self.value)

    @property
    @abstractmethod
    def value(self):
        pass
