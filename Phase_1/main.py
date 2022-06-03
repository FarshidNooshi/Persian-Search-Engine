from __future__ import unicode_literals

from Phase_1.src.Utils.QueryHandler import QueryHandler
from Phase_1.src.Utils.SimplePositionalIndex import SimplePositionalIndex
from Phase_1.src.Utils.StopWord import Document
from Phase_1.src.Utils.utilities import read_file, print_results, zipf_law
from Phase_2.src.config import Config

config = Config()
config.set_config('documents_path',
                  '/Volumes/Farshid_SSD/Projects/University/information retrieval/Phase_1/assets/IR_data_news_12k.json')
docs_url, docs_title, docs_content = read_file(config.get_config('documents_path'))

config.set_config('documents',
                  [Document(url, title, content) for url, title, content in zip(docs_url, docs_title, docs_content)])

pos_index = SimplePositionalIndex(config)

if config.get_config('show_zipf_law'):
    # un comment this line to see the zipf law before removing stop words
    # occurrences = [info['total occurrences'] for info in (pos_index.positional_index_structure.values())]
    # zipf_law(occurrences, 'Zipf plot before stopwords removal')

    occurrences = [info['total occurrences'] for info in (pos_index.positional_index_structure.values())]
    zipf_law(occurrences, 'Zipf plot after stopwords removal')

query_handler = QueryHandler(positional_index=pos_index)

# print_results('تحریم های آمریکا علیه ایران')

# print_results('تحریم های آمریکا ! ایران')

# print_results('"خبرگزاری فارس"')

print_results(query_handler.answer_query('انقلاب')[:config.get_config('documents_to_show')])

# print_results('"مذاکرات وین" توضیحات ! برجام')

# print_results('صهیونیسم ! توکیو')
