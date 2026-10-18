# Проект «Пицца»

Консольное приложение пиццерии: меню с рецептами, заказ пиццы нужного размера с доставкой или самовывозом.

## Требования

- Python 3.10+
- Зависимости из `requirements.txt`

## Установка

```bash
cd pizza
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


## Запуск

```bash
python cli.py menu
python cli.py order pepperoni --delivery
python cli.py order hawaiian --size XL
python cli.py --help
```

## Тесты

```bash
pytest
```

## Проверка кода

```bash
flake8 .
mypy .
```

## Структура

| Файл | Что внутри |
|---|---|
| `recipes.py` | Классы пицц: рецепты, размеры |
| `log.py` | Декоратор, который выводит время выполнения |
| `cli.py` | Команды `menu` и `order` |
| `test_recipes.py`, `test_log.py`, `test_cli.py` | Тесты |

## Примеры вызова

```bash
python cli.py order hawaiian --size XL
python cli.py --help
```
