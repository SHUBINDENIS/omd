import argparse
import csv
from pathlib import Path
from typing import TypedDict


INPUT_FILE = str(Path(__file__).with_name('Corp_Summary.csv'))
OUTPUT_FILE = 'department_summary.csv'


class Summary(TypedDict):
    department: str
    count: int
    min_salary: int
    max_salary: int
    average_salary: float


def read_employees(path: str = INPUT_FILE) -> list[dict[str, str]]:
    with open(path, encoding='utf-8-sig', newline='') as file:
        rows = csv.reader(file, delimiter=';')
        header = next(rows)
        return [dict(zip(header, row)) for row in rows if row]


def build_hierarchy(employees: list[dict[str, str]]) -> dict[str, set[str]]:
    hierarchy: dict[str, set[str]] = {}
    for employee in employees:
        department = employee['Департамент']
        hierarchy.setdefault(department, set()).add(employee['Отдел'])
    return hierarchy


def build_summary(employees: list[dict[str, str]]) -> list[Summary]:
    salaries: dict[str, list[int]] = {}
    for employee in employees:
        department = employee['Департамент']
        salaries.setdefault(department, []).append(int(employee['Оклад']))
    return [
        {
            'department': department,
            'count': len(values),
            'min_salary': min(values),
            'max_salary': max(values),
            'average_salary': sum(values) / len(values),
        }
        for department, values in sorted(salaries.items())
    ]


def print_hierarchy(hierarchy: dict[str, set[str]]) -> None:
    for department, teams in sorted(hierarchy.items()):
        print(department)
        for team in sorted(teams):
            print(f'  {team}')


def print_summary(summary: list[Summary]) -> None:
    print('Департамент | Численность | Минимум | Максимум | Средняя')
    for row in summary:
        print(
            '{department} | {count} | {min_salary} | {max_salary} | '
            '{average_salary:.2f}'.format(**row)
        )


def save_summary(summary: list[Summary], path: str = OUTPUT_FILE) -> None:
    fields = [
        'department', 'count', 'min_salary', 'max_salary', 'average_salary',
    ]
    with open(path, 'w', encoding='utf-8-sig', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields, delimiter=';')
        writer.writeheader()
        writer.writerows(
            {**row, 'average_salary': round(row['average_salary'], 2)}
            for row in summary
        )


def make_report(
    variant: int,
    input_path: str = INPUT_FILE,
    output_path: str = OUTPUT_FILE,
) -> None:
    employees = read_employees(input_path)
    if variant == 1:
        print_hierarchy(build_hierarchy(employees))
    elif variant == 2:
        print_summary(build_summary(employees))
    elif variant == 3:
        save_summary(build_summary(employees), output_path)
    else:
        raise ValueError(f'Unknown variant: {variant}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('variant', type=int, choices=[1, 2, 3])
    parser.add_argument('--input', default=INPUT_FILE)
    parser.add_argument('--output', default=OUTPUT_FILE)
    args = parser.parse_args()
    make_report(args.variant, args.input, args.output)


if __name__ == '__main__':
    main()
