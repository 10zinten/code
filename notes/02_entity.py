"""
Use term `entity` to a domain object that has long-lived identity.
    - unlike values, have `identitu equality

for example:
    1. Person is an entity unlikes names, have an persistent identity
    2. Batch is an entity

"""

from value_object import Name


class Person:
    def __init__(self, name: Name):
        self.name: name

def test_barry_is_harry():
    harry = Person(Name("Harry", "Percival"))
    barry = harry

    barry.name = Name("Barry", "Percival")    # change the name

    assert harry is barry and barry is harry  # identity equality check
