ORDERS = [
    {'id': 1, 'buyer': 'anya', 'status': 'delivered', 'amount': 900},
    {'id': 2, 'buyer': 'boris', 'status': 'returned', 'amount': 4_500},
    {'id': 3, 'buyer': 'anya', 'status': 'delivered', 'amount': 1_500},
    {'id': 4, 'buyer': 'vera', 'status': 'delivered', 'amount': 3_200},
    {'id': 5, 'buyer': 'boris', 'status': 'delivered', 'amount': 700},
    {'id': 6, 'buyer': 'gleb', 'status': 'returned', 'amount': 2_100},
]


def returned_sum():
    return sum(o['amount'] for o in ORDERS if o['status'] == 'returned')


def returned_buyers():
    return {o['buyer'] for o in ORDERS if o['status'] == 'returned'}


def delivered_count():
    return sum(o['status'] == 'delivered' for o in ORDERS)


def delivered_average():
    total = sum(o['amount'] for o in ORDERS if o['status'] == 'delivered')
    return total / delivered_count()


def main():
    print(returned_sum())
    print(returned_buyers())
    print(delivered_count())
    print(delivered_average())


if __name__ == '__main__':
    main()
