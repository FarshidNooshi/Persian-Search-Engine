from collections import Counter
from math import log

from Phase_1.src.Utils.utilities import preprocess_pipeline


class QueryHandler:
    def __init__(self, positional_index, config):
        self.positional_index = positional_index
        self.config = config

    def answer_query(self, query):
        query = preprocess_pipeline(query)
        terms = query.split()
        if self.config.get_config('champions_list'):
            vector_values = self.tf_idf_calculate_normal(terms)
        else:
            vector_values = self.tf_idf_calculate_champions(terms)
        scores = self.calculate_scores(vector_values)
        return dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))[
               :self.config.get_config('documents_to_show')]

    def tf_idf_calculate_normal(self, terms):
        vector_values = {}
        tf_values = Counter(terms)
        for term in terms:
            positional_index_structure = self.positional_index.positional_index_structure
            if term in positional_index_structure.keys():
                for DOC_URL in positional_index_structure[term]['indexes'].keys():
                    if DOC_URL not in vector_values.keys():
                        vector_values[DOC_URL] = {}
                    vector_values[DOC_URL][term] = \
                        (1 + log(tf_values[term])) * self.positional_index.get_idf_value(term)
        return vector_values

    def tf_idf_calculate_champions(self, terms):
        vector_values = {}
        tf_values = Counter(terms)
        for term in terms:
            if term in self.positional_index.positional_index_structure.keys():
                for DOC_URL in self.positional_index.chamions_list[term]:
                    if DOC_URL not in vector_values.keys():
                        vector_values[DOC_URL] = {}
                    vector_values[DOC_URL][term] = \
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
        for DOC_URL, TERM_SCORES in vector_values.items():
            scores[DOC_URL] = self.cosine_similarity(vector_values[DOC_URL],
                                                     self.positional_index.document_term_tfidf_dictionary[DOC_URL])
        return scores
