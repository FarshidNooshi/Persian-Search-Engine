from collections import Counter
from math import log

from Phase_1.src.Utils.utilities import preprocess_pipeline


class QueryHandler:
    def __init__(self, positional_index, config):
        self.positional_index = positional_index
        self.config = config

    def answer_query(self, query):
        query = preprocess_pipeline(query)
        print(f'Query: {query}\n\n\n')
        terms = query.split()
        vector_values = self.tf_idf_calculate(terms, self.config.get_config('champions_list'))
        scores = self.calculate_scores(vector_values)
        results_url = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True)[
                           :self.config.get_config('documents_to_show')])
        total_results = self.generate_total_results(results_url)
        return total_results

    def generate_total_results(self, results_url):
        total_results = []
        for URL, SCORE in results_url.items():
            result = self.positional_index.url_to_information[URL]
            result['score'] = SCORE
            result['url'] = URL
            total_results.append(result)
        return total_results

    def tf_idf_calculate(self, terms, champions_list):
        vector_values = {}
        tf_values = Counter(terms)
        for term in terms:
            for DOC_URL in self.get_search_dict_list(champions_list, term):
                if DOC_URL not in vector_values.keys():
                    vector_values[DOC_URL] = {}
                vector_values[DOC_URL][term] = \
                    (log(1 + tf_values[term])) * self.positional_index.get_idf_value(term)
        return vector_values

    def get_search_dict_list(self, champions_list, term):
        if champions_list and term in self.positional_index.champions_list.keys():
            return self.positional_index.champions_list[term]
        if term in self.positional_index.positional_index_structure.keys():
            return self.positional_index.positional_index_structure[term]['indexes']
        return None

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

