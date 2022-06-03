from math import log

from Phase_1.src.Utils.SimplePositionalIndex import SimplePositionalIndex


class DevelopedPositionalIndex(SimplePositionalIndex):
    def __init__(self, documents_url, documents_title, documents_content):
        super().__init__(documents_url, documents_title, documents_content)
        self.total_number_of_documents = len(documents_url)
        self.build_updated_positional_index()

    def build_updated_positional_index(self):
        for word in self.positional_index_structure.keys():
            number_of_unique_occurrences = len(self.positional_index_structure[word]['indexes'])
            for doc_url, dictionary in self.positional_index_structure[word]['indexes'].items():
                dictionary['tf idf'] = (1 + log(dictionary['number of occurrences in document'])) * \
                                       log(self.total_number_of_documents / number_of_unique_occurrences)
