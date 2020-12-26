"""
Value Object:
    - Any object that is identified only buy it's data and doesn't have long-lived identity
    - Domain object that is uniquely identified by the data it holds; we usually make them immutable

Dataclasses (or namedtuples) are great for Value Object
    - It give us is the value equality (i.e., two objects with same data are equal)

"""

from collections import namedtuple
from dataclasses import dataclass
from typing import NamedTuple

import pytest


@dataclass(frozen=True)
class Name:
    frist_name: str
    surname: str

class Money(NamedTuple):
    currency: str
    value: int

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Should be in same currency")
        return Money(self.currency, self.value+other.value)

    def __sub__(self, other):
        if self.currency != other.currency:
            raise ValueError("Should be in same currency")
        return Money(self.currency, self.value-other.value)

    def __mul__(self, scalar):
        if not isinstance(scalar, int):
            raise TypeError("Should be scalar")
        return Money(self.currency, self.value*scalar)



Line = namedtuple('Line', ['sku', 'qty'])

def test_equality():
    assert Name("Tenzin", "Sonam") != Name("Tenzin", "Tsering")
    assert Money('gbp', 10) == Money('gbp', 10)
    assert Line('RED-CHAIR', 5) == Line('RED-CHAIR', 5)


fiver = Money('gbp', 5)
tenner = Money('gbp', 10)

def test_can_add_money_values_for_the_same_currency():
    assert fiver + fiver == tenner

def test_can_subtract_money_values():
    assert tenner - fiver == fiver

def test_cannot_add_different_currencies():
    with pytest.raises(ValueError):
        Money('usd', 10) + Money('gbp', 10)

def test_can_multiply_money_by_a_number():
    assert fiver * 5 == Money('gbp', 25)

def test_cannot_multiply_two_money_values():
    with pytest.raises(TypeError):
        tenner * fiver
