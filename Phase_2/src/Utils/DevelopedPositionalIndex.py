from math import log

from Phase_1.src.Utils.SimplePositionalIndex import SimplePositionalIndex


class DevelopedPositionalIndex(SimplePositionalIndex):
    def __init__(self, documents_url, documents_title, documents_content):
        super().__init__(documents_url, documents_title, documents_content, False)
        self.total_number_of_documents = len(documents_url)
        self.document_term_tfidf_dictionary = {}
        self.build_updated_positional_index()

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
