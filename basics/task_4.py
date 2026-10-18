DAYS = [
    {'day': 'пн', 'orders': 20, 'revenue': 40_000, 'returns': 2},
    {'day': 'вт', 'orders': 16, 'revenue': 19_200, 'returns': 4},
    {'day': 'ср', 'orders': 25, 'revenue': 55_000, 'returns': 1},
    {'day': 'чт', 'orders': 10, 'revenue': 12_000, 'returns': 3},
    {'day': 'пт', 'orders': 30, 'revenue': 48_000, 'returns': 3},
]


def weekly_revenue():
    return sum(d['revenue'] for d in DAYS)


def best_day():
    return max(DAYS, key=lambda d: d['revenue'])['day']


def revenue_per_order():
    return {d['day']: d['revenue'] / d['orders'] for d in DAYS}


def high_return_days():
    return [d['day'] for d in DAYS if d['returns'] / d['orders'] > 0.2]


def main():
    print(weekly_revenue())
    print(best_day())
    print(revenue_per_order())
    print(high_return_days())


if __name__ == '__main__':
    main()
