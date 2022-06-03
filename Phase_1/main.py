from __future__ import unicode_literals

from Phase_1.src.Utils.PositionalIndex import PositionalIndex
from Phase_1.src.Utils.QueryHandler import QueryHandler
from Phase_1.src.Utils.utilities import read_file, print_results, zipf_law

docs_url, docs_title, docs_content = read_file()

pos_index = PositionalIndex(documents_url=docs_url, documents_title=docs_title, documents_content=docs_content)

# pos2_index = PositionalIndex(documents_url=docs_url, documents_title=docs_title, documents_content=docs_content)
# occurrences = [info['total occurrences'] for info in (pos2_index.positional_index_structure.values())]
# zipf_law(occurrences, 'Zipf plot before stopwords removal')

occurrences = [info['total occurrences'] for info in (pos_index.positional_index_structure.values())]
zipf_law(occurrences, 'Zipf plot after stopwords removal')

query_handler = QueryHandler(positional_index=pos_index)

# print_results('تحریم های آمریکا علیه ایران')

# print_results('تحریم های آمریکا ! ایران')

# print_results('"خبرگزاری فارس"')

print_results(query_handler, '"کنگره ضدتروریست "')

# print_results('"مذاکرات وین" توضیحات ! برجام')

# print_results('صهیونیسم ! توکیو')
