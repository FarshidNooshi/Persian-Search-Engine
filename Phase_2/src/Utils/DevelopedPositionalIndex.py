import math

from Phase_1.src.Utils.SimplePositionalIndex import SimplePositionalIndex
from Phase_1.src.Utils.StopWord import Document
from Phase_1.src.Utils.utilities import read_file
from Phase_2.src.config import Config


class DevelopedPositionalIndex(SimplePositionalIndex):
    def __init__(self, configurations):
        super().__init__(configurations)
        self.total_number_of_documents = len(self.Documents)
        self.document_term_tfidf_dictionary = {}
        self.build_updated_positional_index()
        if configurations.get_config('champions_list'):
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
        return math.log(1 + self.positional_index_structure[word]['indexes'][url]['number of occurrences in document'])

    def get_idf_value(self, word):
        return math.log(self.total_number_of_documents / len(self.positional_index_structure[word]['indexes']))

    def build_champions_list(self):
        champions_list = {}
        for WORD in self.positional_index_structure.keys():
            url_tf_dictionary = {}
            for DOC_URL, DICTIONARY in self.positional_index_structure[WORD]['indexes'].items():
                url_tf_dictionary[DOC_URL] = self.get_tf_value(WORD, DOC_URL)
            champions_list_size = int(
                self.config.get_config('champions_lists_ratio') * len(self.positional_index_structure[WORD]['indexes']))
            champions_list[WORD] = sorted(url_tf_dictionary, key=lambda item: item[1], reverse=True)[
                                   :champions_list_size]
        return champions_list


config = Config()
config.set_config('documents_path',
                  '/Volumes/Farshid_SSD/Projects/University/information retrieval/Phase_1/assets/IR_data_news_12k.json')
docs_url, docs_title, docs_content = read_file(config.get_config('documents_path'))

config.set_config('documents',
                  [Document(content, url, title) for url, title, content in zip(docs_url, docs_title, docs_content)])
config.set_config('champions_list', True)

pos_index = DevelopedPositionalIndex(config)
