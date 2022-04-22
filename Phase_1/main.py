from __future__ import unicode_literals

import json
from os import path
import codecs
from Phase_1.src.utils import data_path
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


default_stop_words = path.join(data_path, 'stopwords.dat')


class StopWord:
    """ Class for remove stop words

         >>> StopWord().clean(["در","تهران","کی","بودی؟"])
         ['تهران', 'کی', 'بودی؟']
         >>> StopWord(normal=True).clean(["در","تهران","کی","بودی؟"])
         ['تهران', 'بودی؟']

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
