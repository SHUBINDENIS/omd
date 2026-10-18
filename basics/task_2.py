QUERIES = [
    'чехол',
    'iphone',
    'чехол',
    'наушники',
    'iphone',
    'iphone',
    'кабель',
    'чехол',
    'iphone',
]


def total_queries():
    return len(QUERIES)


def query_counts():
    counts = {}
    for query in QUERIES:
        counts[query] = counts.get(query, 0) + 1
    return counts


def most_frequent():
    counts = query_counts()
    query = max(counts, key=counts.get)
    return query, counts[query] / total_queries()


def single_queries():
    return [q for q, count in query_counts().items() if count == 1]


def main():
    print(total_queries())
    print(query_counts())
    print(most_frequent())
    print(single_queries())


if __name__ == '__main__':
    main()
