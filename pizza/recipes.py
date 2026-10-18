from typing import ClassVar


class Pizza:
    SIZES: ClassVar[tuple[str, ...]] = ('L', 'XL')
    ingredients: ClassVar[tuple[str, ...]] = ()
    emoji: ClassVar[str] = ''

    def __init__(self, size: str = 'L') -> None:
        if size not in self.SIZES:
            raise ValueError('Допустимые размеры: ' + ', '.join(self.SIZES))
        self._size = size

    @property
    def size(self) -> str:
        return self._size

    @property
    def name(self) -> str:
        return type(self).__name__

    def dict(self) -> dict[str, tuple[str, ...]]:
        return {self.name: self.ingredients}

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pizza):
            return NotImplemented
        return type(self) is type(other) and self.size == other.size

    def __hash__(self) -> int:
        return hash((type(self), self.size))


class Margherita(Pizza):
    ingredients = ('tomato sauce', 'mozzarella', 'tomatoes')
    emoji = '🧀'


class Pepperoni(Pizza):
    ingredients = ('tomato sauce', 'mozzarella', 'pepperoni')
    emoji = '🍕'


class Hawaiian(Pizza):
    ingredients = ('tomato sauce', 'mozzarella', 'chicken', 'pineapples')
    emoji = '🍍'
