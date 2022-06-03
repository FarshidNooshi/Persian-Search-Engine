from Phase_1.src.Utils.StopWord import Document
from Phase_1.src.Utils.utilities import read_file, print_results
from Phase_2.src.Utils.DevelopedPositionalIndex import DevelopedPositionalIndex
from Phase_2.src.Utils.QueryHandler import QueryHandler
from Phase_2.src.config import Config

config = Config()
docs_url, docs_title, docs_content = read_file(config.get_config('documents_path'))

config.set_config('documents',
                  [Document(url, title, content) for url, title, content in zip(docs_url, docs_title, docs_content)])

pos_index = DevelopedPositionalIndex(config)


query_handler = QueryHandler(pos_index, config)
# print(query_handler.answer_query('انقلاب اسلامی ایران'))
print_results(query_handler.answer_query('انقلاب'))

