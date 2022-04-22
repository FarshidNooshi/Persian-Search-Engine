from __future__ import unicode_literals

import json
from hazm import *


def read_file():
    docs_title = []
    docs_content = []
    docs_url = []
    with open('assets/IR_data_news_12k.json', encoding='UTF-8') as f:
        data = json.load(f)
        for i in data:
            docs_title.append(data[i]["title"])
            docs_content.append(data[i]["content"])
            docs_url.append(data[i]['url'])
    return docs_url, docs_title, docs_content


normalizer = Normalizer()
