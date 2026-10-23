import argparse

INPUT_FILE = 'Corp_Summary.csv'
OUTPUT_FILE = 'department_summary.csv'


def read_employees(path: str = INPUT_FILE) -> list[dict]:
    raise NotImplementedError


def build_hierarchy(employees: list[dict]) -> dict[str, set[str]]:
    raise NotImplementedError


def build_summary(employees: list[dict]) -> list[dict]:
    raise NotImplementedError


def print_hierarchy(hierarchy: dict[str, set[str]]) -> None:
    raise NotImplementedError


def print_summary(summary: list[dict]) -> None:
    raise NotImplementedError


def save_summary(summary: list[dict], path: str = OUTPUT_FILE) -> None:
    raise NotImplementedError


def make_report(variant: int, input_path: str = INPUT_FILE,
                output_path: str = OUTPUT_FILE) -> None:
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
