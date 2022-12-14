"""Hash table implementation of a set."""

from typing import (
    Generic, Iterable, TypeVar, Iterator
)

T = TypeVar('T')


class HashSet2(Generic[T]):
    """Set implementation using a hash table."""

    size: int
    used: int
    array: list[list[T]]

    def __init__(self, seq: Iterable[T] = (), initial_size: int = 16):
        """Create a set from a sequence, optionally with a specified size."""
        seq = list(seq)

        if 2 * len(seq) > initial_size:
            initial_size = 2 * len(seq)

        self.size = initial_size
        self.used = 0
        self.array = [list() for _ in range(initial_size)]

        for value in seq:
            self.add(value)

    def _get_bin(self, hash_val) -> list[T]: # The hash value should already be stored with the element, so we can simply use that value to get the index
        """Get the list (bin) that element should sit in."""
        #hash_val = hash(element)
        index = hash_val % self.size
        return self.array[index]

    def _resize(self, new_size: int) -> None:
        """Change the table size to new_size bins."""
        old_array = self.array
        self.size = new_size
        self.used = 0
        self.array = [list() for _ in range(new_size)]
        for b in old_array:
            for (x, h) in b:
                b = self._get_bin(h)
                b.append((x, h))
                self.used += 1

    def add(self, element: T) -> None:
        """Add element to the set."""
        h = hash(element)
        b = self._get_bin(h)
        if (element, h) not in b:
            b.append((element, h))
            self.used += 1
            if self.used > self.size / 2:
                self._resize(int(2 * self.size))

    def remove(self, element: T) -> None:
        """Remove element from the set."""
        h = hash(element)
        b = self._get_bin(h)
        if (element, h) not in b:
            raise KeyError((element, h))
        b.remove((element, h))
        self.used -= 1
        if self.used < self.size / 4:
            self._resize(int(self.size / 2))

    def __iter__(self) -> Iterator[T]:
        """Iterate through all the elements in the set."""
        for b in self.array:
            yield from (element for (element, h) in b)

    def __bool__(self) -> bool:
        """Test if the set is non-empty."""
        return self.used > 0

    def __contains__(self, element: T) -> bool:
        """Test if element is in the set."""
        h = hash(element)
        b = self._get_bin(h)
        return (element, h) in b

    def __repr__(self) -> str:
        """Get representation string."""
        return 'HashTableSet(' + repr(tuple(self)) + ')'
