# coding: utf8
import codecs
from os import path

from hazm.Normalizer import Normalizer

from Phase_1.src.creds import data_path

default_stop_words = path.join(data_path, 'stopwords.dat')


class StopWord:
    """ Class for remove stop words

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


class Document:
    def __init__(self, content, url, title):
        self.content = content
        self.url = url
        self.title = title
