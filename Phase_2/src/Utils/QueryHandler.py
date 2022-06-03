from collections import Counter
from math import log

from Phase_1.src.Utils.utilities import preprocess_pipeline


class QueryHandler:
    def __init__(self, positional_index):
        self.positional_index = positional_index

    def answer_query(self, query):
        query = preprocess_pipeline(query)
        terms = query.split()
        vector_values = self.tf_idf_calculate(terms)
        scores = self.calculate_scores(vector_values)
        return scores

    def tf_idf_calculate(self, terms):
        vector_values = {}
        tf_values = Counter(terms)
        for term in terms:
            positional_index_structure = self.positional_index.positional_index_structure
            vector_values[term] = {}
            if term in positional_index_structure.keys():
                for DOC_URL in positional_index_structure[term]['indexes'].keys():
                    vector_values[term][DOC_URL] = \
                        (1 + log(tf_values[term])) * self.positional_index.get_idf_value(term)
        return vector_values

    @staticmethod
    def cosine_similarity(v1, v2):
        dot_product = 0
        for term in v1.keys():
            if term in v2.keys():
                dot_product += v1[term] * v2[term]
        magnitude_v1 = 0
        for term in v1.keys():
            magnitude_v1 += v1[term] ** 2
        magnitude_v2 = 0
        for term in v2.keys():
            magnitude_v2 += v2[term] ** 2
        return dot_product / (magnitude_v1 ** 0.5) / (magnitude_v2 ** 0.5)

    def calculate_scores(self, vector_values):
        scores = {}
        for DOC_URL, TERM_SCORES in self.positional_index.document_term_tfidf_dictionary.items():
            scores[DOC_URL] = self.cosine_similarity(vector_values, TERM_SCORES)
        return scores
