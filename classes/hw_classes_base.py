from math import log


class CountVectorizer:
    def __init__(self, lowercase=True, ngram_size=1):
        if type(ngram_size) is not int or ngram_size not in (1, 2):
            raise ValueError('ngram_size must be 1 or 2')
        self.lowercase = lowercase
        self.ngram_size = ngram_size
        self._vocabulary = {}
        self._ready = False

    @property
    def vocabulary(self):
        return self._vocabulary.copy()

    @vocabulary.setter
    def vocabulary(self, vocabulary):
        indices = list(vocabulary.values())
        if any(type(index) is not int for index in indices):
            raise ValueError('Vocabulary indices must be integers')
        if len(set(indices)) != len(indices):
            raise ValueError('Vocabulary indices must be unique')
        if sorted(indices) != list(range(len(indices))):
            raise ValueError('Vocabulary indices must be consecutive from 0')
        self._vocabulary = dict(vocabulary)
        self._ready = True

    @vocabulary.deleter
    def vocabulary(self):
        self._vocabulary = {}
        self._ready = False

    def add_word(self, word):
        return self._vocabulary.setdefault(word, len(self._vocabulary))

    def tokenize(self, text):
        if self.lowercase:
            text = text.lower()
        words = text.split()
        if self.ngram_size == 1:
            return words
        return [f'{left} {right}' for left, right in zip(words, words[1:])]

    def fit(self, corpus):
        candidate = CountVectorizer(self.lowercase, self.ngram_size)
        for text in corpus:
            for token in self.tokenize(text):
                candidate.add_word(token)
        if not candidate._vocabulary:
            raise ValueError('The training corpus contains no tokens')
        self.vocabulary = candidate._vocabulary
        return self

    def transform(self, corpus):
        if not self._ready:
            raise RuntimeError('Fit the vectorizer or set its vocabulary')
        matrix = []
        for text in corpus:
            row = [0] * len(self._vocabulary)
            for token in self.tokenize(text):
                index = self._vocabulary.get(token)
                if index is not None:
                    row[index] += 1
            matrix.append(row)
        return matrix

    def get_feature_names(self):
        return sorted(self._vocabulary, key=self._vocabulary.__getitem__)

    def fit_transform(self, corpus):
        corpus = list(corpus)
        return self.fit(corpus).transform(corpus)

    def to_dict(self):
        return {
            'lowercase': self.lowercase,
            'ngram_size': self.ngram_size,
            'vocabulary': self.vocabulary,
        }

    @classmethod
    def from_dict(cls, state):
        vectorizer = cls(
            lowercase=state['lowercase'], ngram_size=state['ngram_size']
        )
        vectorizer.vocabulary = state['vocabulary']
        return vectorizer


class BinaryVectorizer(CountVectorizer):
    def transform(self, corpus):
        return [[int(count > 0) for count in row]
                for row in super().transform(corpus)]


class TfidfVectorizer(CountVectorizer):
    def __init__(self, lowercase=True, use_idf=True, ngram_size=1):
        super().__init__(lowercase, ngram_size)
        self.use_idf = use_idf
        self._idf = []

    @CountVectorizer.vocabulary.setter
    def vocabulary(self, vocabulary):
        CountVectorizer.vocabulary.fset(self, vocabulary)
        self._idf = []

    @vocabulary.deleter
    def vocabulary(self):
        CountVectorizer.vocabulary.fdel(self)
        self._idf = []

    @property
    def idf(self):
        return self._idf.copy()

    def to_dict(self):
        state = super().to_dict()
        state['use_idf'] = self.use_idf
        state['idf'] = self.idf
        return state

    @classmethod
    def from_dict(cls, state):
        vectorizer = super().from_dict(state)
        vectorizer.use_idf = state.get('use_idf', True)
        vectorizer._idf = list(state.get('idf', ()))
        return vectorizer

    @classmethod
    def from_config(cls, config):
        return cls(
            lowercase=config.get('lowercase', True),
            use_idf=config.get('use_idf', True),
            ngram_size=config.get('ngram_size', 1),
        )

    def fit(self, corpus):
        corpus = list(corpus)
        super().fit(corpus)
        self._idf = []
        if self.use_idf:
            counts = super().transform(corpus)
            self._idf = [
                log((len(corpus) + 1)
                    / (sum(count > 0 for count in column) + 1)) + 1
                for column in zip(*counts)
            ]
        return self

    def transform(self, corpus):
        counts = super().transform(corpus)
        if self.use_idf and len(self._idf) != len(self._vocabulary):
            raise RuntimeError('Fit the vectorizer to calculate IDF weights')
        weights = self._idf if self.use_idf else [1.0] * len(self._vocabulary)
        matrix = []
        for row in counts:
            total = sum(row)
            if total:
                matrix.append([
                    count / total * weight
                    for count, weight in zip(row, weights)
                ])
            else:
                matrix.append([0.0] * len(row))
        return matrix


class KeywordExtractor:
    def __init__(self, vectorizer, top_n=3):
        self.vectorizer = vectorizer
        self.top_n = top_n

    @property
    def top_n(self):
        return self._top_n

    @top_n.setter
    def top_n(self, value):
        if type(value) is not int or value <= 0:
            raise ValueError('top_n must be a positive integer')
        self._top_n = value

    def fit(self, corpus):
        self.vectorizer.fit(corpus)
        return self

    def extract(self, corpus):
        names = self.vectorizer.get_feature_names()
        result = []
        for row in self.vectorizer.transform(corpus):
            candidates = [(name, weight) for name, weight in zip(names, row)
                          if weight > 0]
            candidates.sort(key=lambda pair: (-pair[1], pair[0]))
            result.append(candidates[:self.top_n])
        return result


def demo():
    train_corpus = [
        'Марс сигнал сигнал', 'Марс пыль', 'Марс сигнал антенна',
    ]
    check_corpus = [
        'СИГНАЛ шум сигнал', 'антенна пыль', 'марс марс марс', 'комета', '',
    ]

    # Проверьте веса на обучающих и новых текстах и независимость копии IDF.
    print('1. Веса TF-IDF')
    tfidf = TfidfVectorizer.from_config({})
    train_matrix = tfidf.fit_transform(train_corpus)
    print('Слова:', tfidf.get_feature_names())
    print('IDF:', tfidf.idf)
    print('Обучающая матрица:', train_matrix)
    print('Проверочная матрица:', tfidf.transform(check_corpus))
    idf_copy = tfidf.idf
    idf_copy.clear()
    print('IDF после очистки копии:', tfidf.idf)

    # Сравните TF с учётом регистра и проверьте замену словаря после fit.
    print('\n2. Настройки и повторное обучение')
    tf = TfidfVectorizer.from_config({
        'lowercase': False, 'use_idf': False,
    })
    tf_matrix = tf.fit_transform(['Марс марс', 'МАРС сигнал'])
    print('Слова:', tf.get_feature_names())
    print('IDF:', tf.idf)
    print('TF:', tf_matrix)
    tfidf.fit(['Венера облака'])
    print('Новые слова:', tfidf.get_feature_names())
    print('Новые IDF:', tfidf.idf)
    print('Матрица:', tfidf.transform(['Марс Венера облака']))

    # При равных весах порядок слов определяет алфавит.
    print('\n3. Ключевые слова')
    extractor = KeywordExtractor(tfidf, top_n=2).fit(train_corpus)
    print('top_n=2:', extractor.extract(check_corpus))
    extractor.top_n = 1
    print('top_n=1:', extractor.extract(check_corpus))
    try:
        extractor.top_n = 0
    except ValueError as error:
        print('top_n=0:', error)


if __name__ == '__main__':
    demo()
