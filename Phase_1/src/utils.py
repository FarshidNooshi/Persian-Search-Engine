# coding: utf8
from __future__ import unicode_literals

from os import path
from hazm import *
import json


def read_file():
    documents_title = []
    documents_content = []
    documents_url = []
    with open('../Phase_1/assets/IR_data_news_12k.json', encoding='UTF-8') as f:
        data = json.load(f)
        for i in data:
            documents_title.append(data[i]["title"])
            documents_content.append(data[i]["content"])
            documents_url.append(data[i]['url'])
    return documents_url, documents_title, documents_content


data_path = path.join(path.dirname(__file__), 'data')
default_stop_words = path.join(data_path, 'stopwords.dat')
normalizer = Normalizer()

