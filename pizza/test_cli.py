from unittest.mock import patch

import pytest
from click.testing import CliRunner

from cli import cli


def test_menu() -> None:
    result = CliRunner().invoke(cli, ['menu'])
    assert result.exit_code == 0
    assert result.output == (
        '- Margherita 🧀: tomato sauce, mozzarella, tomatoes\n'
        '- Pepperoni 🍕: tomato sauce, mozzarella, pepperoni\n'
        '- Hawaiian 🍍: tomato sauce, mozzarella, chicken, pineapples\n'
    )


@pytest.mark.parametrize('pizza', ['margherita', 'pepperoni', 'hawaiian'])
@pytest.mark.parametrize('delivery', [False, True])
def test_order(pizza: str, delivery: bool) -> None:
    arguments = ['order', pizza, '--size', 'XL']
    if delivery:
        arguments.append('--delivery')

    with patch('log.random.randint', return_value=2):
        result = CliRunner().invoke(cli, arguments)

    assert result.exit_code == 0
    assert f'Готовим {pizza.title()} (XL)' in result.output
    assert '👨‍🍳 Приготовили за 2с!' in result.output
    expected = '🛵 Доставили за 2с!' if delivery else '🏠 Забрали за 2с!'
    unexpected = '🏠 Забрали за 2с!' if delivery else '🛵 Доставили за 2с!'
    assert expected in result.output
    assert unexpected not in result.output


def test_default_size() -> None:
    result = CliRunner().invoke(cli, ['order', 'Margherita'])
    assert result.exit_code == 0
    assert 'Margherita (L)' in result.output


@pytest.mark.parametrize(
    'arguments',
    [
        ['order', 'unknown'],
        ['order', 'margherita', '--size', 'M'],
    ],
)
def test_invalid_order(arguments: list[str]) -> None:
    assert CliRunner().invoke(cli, arguments).exit_code == 2


def test_help() -> None:
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Пиццерия: меню и заказы.' in result.output
    assert 'Показать меню с составом пицц.' in result.output
    assert 'Заказать пиццу.' in result.output
    result = runner.invoke(cli, ['order', '--help'])
    assert result.exit_code == 0
    assert 'Доставка курьером.' in result.output
    assert 'Размер пиццы.' in result.output
