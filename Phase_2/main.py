from Phase_1.src.Utils.StopWord import Document
from Phase_1.src.Utils.utilities import read_file, print_results
from Phase_2.src.Utils.DevelopedPositionalIndex import DevelopedPositionalIndex
from Phase_2.src.Utils.QueryHandler import QueryHandler
from Phase_2.src.config import Config

config = Config()
config.set_config('documents_path',
                  '/Volumes/Farshid_SSD/Projects/University/information retrieval/Phase_1/assets/IR_data_news_12k.json')
docs_url, docs_title, docs_content = read_file(config.get_config('documents_path'))

config.set_config('documents',
                  [Document(content, url, title) for url, title, content in zip(docs_url, docs_title, docs_content)])
config.set_config('champions_list', True)

pos_index = DevelopedPositionalIndex(config)

query_handler = QueryHandler(pos_index, config)
print_results(query_handler.answer_query('مجلس'))

