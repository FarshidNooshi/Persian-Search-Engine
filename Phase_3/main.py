from __future__ import unicode_literals

import json
import os

# %pip install -U hazm
from hazm import *

os.chdir('../')


def read_file():
    documents_title = []
    documents_content = []
    documents_url = []
    with open(os.path.join(os.getcwd(), 'Phase_1', 'assets', 'IR_data_news_12k.json'), encoding='UTF-8') as f:
        data = json.load(f)
        for i in data:
            documents_title.append(data[i]["title"])
            documents_content.append(data[i]["content"])
            documents_url.append(data[i]['url'])
    return documents_url, documents_title, documents_content


docs_url, docs_title, docs_content = read_file()
normalizer = Normalizer()

# coding: utf8
from os import path
import codecs
from hazm.Normalizer import Normalizer

# from Phase_1.src.utils import data_path
default_stop_words = path.join(os.getcwd(), 'Phase_1', 'src', 'data', 'stopwords.dat')


class StopWord:
    """ Class for remove stop words

         >>> StopWord().clean(["در","تهران","کی","بودی؟"])
         ['بودی؟', 'تهران', 'کی']
         >>> StopWord(normal=True).clean(["در","تهران","کی","بودی؟"])
         ['بودی؟', 'تهران']

         """

    def __init__(self, file_path=default_stop_words, normal=False):
        self.file_path = file_path
        self.normal = normal
        self.normalizer = Normalizer().normalize
        self.stop_words = self.init(file_path, normal)

    def init(self, file_path, normal):
        if not normal:
            return set(
                line.strip("\r\n") for line in codecs.open(file_path, "r", encoding="utf-8").readlines())
        else:
            return set(
                self.normalizer(line.strip("\r\n")) for line in
                codecs.open(file_path, "r", encoding="utf-8").readlines())

    def set_normalizer(self, func):
        self.normalizer = func
        self.stop_words = self.init(self.file_path, self.normal)

    def __getitem__(self, item):
        return item in self.stop_words

    def __str__(self):
        return str(self.stop_words)

    def clean(self, iterable_of_strings, return_generator=False):
        if return_generator:
            return filter(lambda item: not self[item], iterable_of_strings)
        else:
            return list(filter(lambda item: not self[item], iterable_of_strings))


def preprocess_content(content):
    str_empty = ' '
    stemmer = Stemmer()
    content = normalizer.normalize(content)
    content = word_tokenize(content)
    content = StopWord(normal=False).clean(content)
    content = [stemmer.stem(word) for word in content]
    content = str_empty.join(content)
    return content


for doc_content in docs_content:
    doc_content = preprocess_content(doc_content)


class Document:
    def __init__(self, content, url, title):
        self.content = content
        self.url = url
        self.title = title


from elasticsearch import Elasticsearch, helpers

# Connect to 'http://localhost:9200'
es = Elasticsearch("http://localhost:55000")

import uuid


def generate_data():
    data = []
    for doc_content, doc_url, doc_title in zip(docs_content, docs_url, docs_title):
        if doc_content and doc_url and doc_title:
            data.append({
                "_index": "IR-Phase-3",
                "_id": uuid.uuid4(),
                # "doc_type" : "document",
                "doc": {
                    "content": doc_content,
                    "url": doc_url,
                    "title": doc_title
                }
            })
    return data


data = generate_data()
print(data)
response = helpers.bulk(es, data, index="IR-Phase-3")
#
# from datetime import datetime
#
# actions = [
#     {
#         "_index": "tickets-index",
#         "_id": j,
#         "_source": {
#             "any": "data" + str(j),
#             "timestamp": datetime.now()}
#     }
#     for j in range(0, 10)
# ]
#
# helpers.bulk(es, actions)
