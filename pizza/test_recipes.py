import pytest

from recipes import Hawaiian, Margherita, Pepperoni, Pizza


@pytest.mark.parametrize(
    ('recipe', 'ingredients'),
    [
        (Margherita, ('tomato sauce', 'mozzarella', 'tomatoes')),
        (Pepperoni, ('tomato sauce', 'mozzarella', 'pepperoni')),
        (Hawaiian, ('tomato sauce', 'mozzarella', 'chicken', 'pineapples')),
    ],
)
def test_dict(recipe: type[Pizza], ingredients: tuple[str, ...]) -> None:
    assert recipe().dict() == {recipe.__name__: ingredients}
    assert recipe().name == recipe.__name__


@pytest.mark.parametrize('recipe', [Margherita, Pepperoni, Hawaiian])
@pytest.mark.parametrize('size', Pizza.SIZES)
def test_sizes(recipe: type[Pizza], size: str) -> None:
    assert recipe(size).size == size


@pytest.mark.parametrize('recipe', [Margherita, Pepperoni, Hawaiian])
@pytest.mark.parametrize('size', ['M', 'l', 'XXL'])
def test_invalid_size(recipe: type[Pizza], size: str) -> None:
    with pytest.raises(ValueError):
        recipe(size)


def test_equality() -> None:
    assert Margherita() == Margherita()
    assert Margherita('XL') == Margherita('XL')
    assert Margherita() != Margherita('XL')
    assert Margherita() != Pepperoni()
    assert Margherita() != object()


def test_hash() -> None:
    assert hash(Margherita()) == hash(Margherita())
    assert len({Margherita(), Margherita()}) == 1
    assert len({Margherita(), Margherita('XL'), Pepperoni()}) == 3


def test_size_is_read_only() -> None:
    with pytest.raises(AttributeError):
        setattr(Margherita(), 'size', 'XL')
