from dataclasses import dataclass
from datetime import date
from typing import List, NewType, Optional, Set

Quantity = NewType("Quantity", int)
Sku = NewType("Sku", str) # product ref
Reference = NewType("Reference", str) # order ref

@dataclass(frozen=True)
class OrderLine:
    """OrderLine is a `value object`."""
    orderid: Reference
    sku: Sku
    qty: Quantity


class Batch:
    """Batch is an `entity`."""
    def __init__(self, ref: Reference, sku: Sku, qty: Quantity, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_quantity = qty
        self._allocations: Set[OrderLine] = set()

    def __eq__(self, other):
        """check for `identity equality`."""
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        """allows set or dict operations with entities.

        attribute(s) used for hash should be entity's
        unique identity over time.

        For batch it's reference.
        TODO:
            1. We should also make referecne read-only.
        """
        return hash(self.reference)

    def __gt__(self, other):
        """To use `sorted` on batches with `self.eta`.

        Magic methods can express domain semantics
        """
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocations)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

class OutOfStock(Exception):
    pass


def allocate(line: OrderLine, batches: List[Batch]) -> str:
    try:
        batch = next(
            b for b in sorted(batches) if b.can_allocate(line)
        )
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")
    batch.allocate(line)
    return batch.reference
