# Python Basic

Домашние задания курса Python Basic. Каждое задание лежит в отдельной папке.

## Требования

- Python 3.10+
- Только стандартная библиотека, зависимости не нужны

## Запуск

```bash
python basics/task_1.py
```

Остальные задачи запускаются так же: `basics/task_2.py` … `basics/task_5.py`.

## Проверка стиля

```bash
pip install flake8
flake8 .
```

## Задания

| Папка | Тема |
|---|---|
| `basics` | Основы языка |
| `functions` | Функции: отчёт по `Corp_Summary.csv` |

## Функции

Положите `Corp_Summary.csv` рядом со скриптом или передайте путь через `--input`.

```bash
python functions/report.py 1
python functions/report.py 2
python functions/report.py 3 --output department_summary.csv
```

1. Иерархия: команды каждого департамента.
2. Сводка по департаментам: численность, минимальная, максимальная и средняя зарплата.
3. Сводка из пункта 2 в csv-файл.
