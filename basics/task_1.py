MOSCOW = {201, 202, 203, 204}
KAZAN = {203, 204, 205, 206}


def all_products():
    return MOSCOW | KAZAN


def moscow_only():
    return MOSCOW - KAZAN


def kazan_only():
    return KAZAN - MOSCOW


def product_count():
    return len(all_products())


def main():
    print(all_products())
    print(moscow_only())
    print(kazan_only())
    print(product_count())


if __name__ == '__main__':
    main()
