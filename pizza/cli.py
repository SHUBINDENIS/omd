from typing import Final

import click

from log import log
from recipes import Hawaiian, Margherita, Pepperoni, Pizza


PIZZAS: Final[dict[str, type[Pizza]]] = {
    'margherita': Margherita,
    'pepperoni': Pepperoni,
    'hawaiian': Hawaiian,
}


@log('👨‍🍳 Приготовили за {}с!')
def bake(pizza: Pizza) -> None:
    click.echo(f'Готовим {pizza.name} ({pizza.size})')


@log('🛵 Доставили за {}с!')
def deliver(pizza: Pizza) -> None:
    click.echo(f'Доставляем {pizza.name} ({pizza.size})')


@log('🏠 Забрали за {}с!')
def pickup(pizza: Pizza) -> None:
    click.echo(f'Самовывоз {pizza.name} ({pizza.size})')


@click.group()
def cli() -> None:
    """Пиццерия: меню и заказы."""


@cli.command()
def menu() -> None:
    """Показать меню с составом пицц."""
    for recipe in PIZZAS.values():
        pizza = recipe()
        composition = ', '.join(pizza.ingredients)
        click.echo(f'- {pizza.name} {pizza.emoji}: {composition}')


@cli.command()
@click.argument('pizza', type=click.Choice(list(PIZZAS), case_sensitive=False))
@click.option('--delivery', is_flag=True, help='Доставка курьером.')
@click.option(
    '--size', type=click.Choice(Pizza.SIZES), default='L',
    show_default=True, help='Размер пиццы.',
)
def order(pizza: str, delivery: bool, size: str) -> None:
    """Заказать пиццу."""
    ordered = PIZZAS[pizza](size)
    bake(ordered)
    if delivery:
        deliver(ordered)
    else:
        pickup(ordered)


if __name__ == '__main__':
    cli()
