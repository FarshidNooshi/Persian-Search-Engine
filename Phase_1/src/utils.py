# coding: utf8
from __future__ import unicode_literals

import json

from hazm import *

from Phase_1.src.Utils.StopWord import StopWord


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


normalizer = Normalizer()


def preprocess_pipeline(content):
    str_empty = ' '
    stemmer = Stemmer()
    content = normalizer.normalize(content)
    content = word_tokenize(content)
    content = StopWord(normal=False).clean(content)
    content = [stemmer.stem(word) for word in content]
    content = str_empty.join(content)
    return content


def process_positions(preprocessed_content):
    positions = {}
    for position_of_word, word in enumerate(preprocessed_content.split()):
        if word and word not in positions:
            positions[word] = []
        positions[word].append(position_of_word)
    return positions


def generate_index(positions, title):
    return {"number of occurrences in document": len(positions),
            "positions": positions,
            "title of document": title}


def heaps_law(dict_size, num_total_tokens, number):
    print(f'at {number}th document we seen {num_total_tokens} total tokens and dictionary size was {dict_size}')


def print_results(query_handler, query_string, number_to_prints=10):
    for single_result in query_handler.answer_query(query_string)[:number_to_prints]:
        print(f"score: {single_result['score']},\n"
              f"url: {single_result['url']},\n"
              f"title: {single_result['title']}\n"
              f'content: {single_result["content"]}\n*********************************************************\n\n')


def zipf_law(frequencies, title):
    from matplotlib import pyplot as plt

    frequencies.sort(reverse=True)

    # enumerate the ranks and frequencies
    rf = [(r + 1, f) for r, f in enumerate(frequencies)]
    rs, fs = zip(*rf)

    plt.clf()
    plt.xscale('log')
    plt.yscale('log')
    plt.title(title)
    plt.xlabel('rank')
    plt.ylabel('frequency')
    plt.plot(rs, fs, 'b-')
    plt.show()
