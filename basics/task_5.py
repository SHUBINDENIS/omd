REVIEWS = [
    {'id': 1, 'product': 'Чехол', 'stars': 5},
    {'id': 1, 'product': 'Чехол', 'stars': 3},
    {'id': 1, 'product': 'Чехол', 'stars': 4},
    {'id': 2, 'product': 'Наушники', 'stars': 2},
    {'id': 2, 'product': 'наушники', 'stars': 2},
    {'id': 2, 'product': 'НАУШНИКИ', 'stars': 5},
    {'id': 3, 'product': 'Планшет', 'stars': 5},
    {'id': 4, 'product': 'Колонка', 'stars': 4},
    {'id': 4, 'product': 'Колонка', 'stars': 4},
    {'id': 5, 'product': 'Кабель', 'stars': 1},
]


def average_ratings(ratings):
    return {p: sum(stars) / len(stars) for p, stars in ratings.items()}


def worst_product(ratings):
    averages = average_ratings(ratings)
    return min(
        (p for p in ratings if len(ratings[p]) >= 2), key=averages.get
    )


def low_ratings():
    count = sum(1 <= r['stars'] <= 2 for r in REVIEWS)
    return count, count / len(REVIEWS)


def main():
    ratings = {}
    for review in REVIEWS:
        product = review['product'].lower()
        ratings.setdefault(product, []).append(review['stars'])
    print(average_ratings(ratings))
    print(worst_product(ratings))
    print(low_ratings())


if __name__ == '__main__':
    main()
