"""
Object Equality
--------------

Equality in python, need to implement
    - `__eq__()` for `==` and `__ne__()` for `!=`. These should return boolean
      if the class knows how to compare itself to other or `NotImplemented` if
      it doesn't.

   - Python3 implement `__ne__()` for us.

   - By default instances are only equal to themselves because `object` class
     compares two instances by their identity.


Object Hashes
-------------

   - It's an integer number representing the value of the object.

   - Obtained using `hash()` function if the object is hashable.

   - To make the object hashable, it has to implement both the `__hash__(self)`
     and the `__eq__(self, other)` methods.

   - Two instances of the same class will always have different hashes, no matter
     what data they carry

   - hashes are importand because sets and dictionaries used them for their lookup
     tables to quickly find their keys.

    Important assumptions made by sets and dictionaries about it's elements

    Assumption 1: The hash of an object must never change during it's lifetime.
"""

class C:
    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f"C({self.x})"

    def __hash__(self):
        return hash(self.x)

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.x == other.x
        )

d = dict()
s = set()
c = C(1)
d[c] = 42
s.add(c)
print(d, s) # ({C(1): 42}, {C(1)})
print(c in s and c in d) # True, c is in both
c.x = 2
print(c in s or c in d) # False, c is in neither!?
print(d, s) # ({C(2): 42}, {C(2)}), but...it's right there!

"""
This explains why all immutable data structures (like tuple or strings) are
hashable while mutable ones like lists or dictionaries aren't
"""
# Equality check
print(C(1) in s or C(1) in d) # False

"""
   Assumption 2: Hashable objects which compare equal must have the same hash value

   if x == y it must follow that hash(x) == hash(y)

   Since that’s not true in our case, we can’t access that object by its hash anymore.
"""

"""Conclusion:

   1. You can't base your hash on mutable values.
   2. Hashes can be less picky than equality checks. (key lookups are always followed
      by an equality check, hash doesn't have to be unique.
   3. You shouldn't compare by value but hash by identity.

   Python3 automatically makes classes unhashable if you didn't implement both
   `__eq__` and `__hash__` but python2 lets you do this.
