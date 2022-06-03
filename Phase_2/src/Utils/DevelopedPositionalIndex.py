from math import log

from Phase_1.src.Utils.SimplePositionalIndex import SimplePositionalIndex


class DevelopedPositionalIndex(SimplePositionalIndex):
    def __init__(self, config):
        super().__init__(config)
        self.total_number_of_documents = len(self.Documents)
        self.document_term_tfidf_dictionary = {}
        self.build_updated_positional_index()
        if config.get_config('champions_list'):
            self.champions_list = self.build_champions_list()

    def build_updated_positional_index(self):
        for WORD in self.positional_index_structure.keys():
            for DOC_URL, DICTIONARY in self.positional_index_structure[WORD]['indexes'].items():
                DICTIONARY['tf idf'] = self.get_tf_value(WORD, DOC_URL) * self.get_idf_value(WORD)
                if DOC_URL not in self.document_term_tfidf_dictionary.keys():
                    self.document_term_tfidf_dictionary[DOC_URL] = {WORD: DICTIONARY['tf idf']}
                else:
                    self.document_term_tfidf_dictionary[DOC_URL][WORD] = DICTIONARY['tf idf']

    def get_tf_value(self, word, url):
        return 1 + log(self.positional_index_structure[word]['indexes'][url]['number of occurrences in document'])

    def get_idf_value(self, word):
        return log(self.total_number_of_documents / len(self.positional_index_structure[word]['indexes']))

    def build_champions_list(self):
        return {}
