# coding: utf8
from __future__ import unicode_literals

import json
import pickle

from parsivar import Normalizer, Tokenizer, FindStems
from Phase_1.src.Utils.StopWord import StopWord


def read_file(path='../Phase_1/assets/IR_data_news_12k.json'):
    documents_title = []
    documents_content = []
    documents_url = []
    with open(path, encoding='UTF-8') as f:
        data = json.load(f)
        for i in data:
            documents_title.append(data[i]["title"])
            documents_content.append(data[i]["content"])
            documents_url.append(data[i]['url'])
    return documents_url, documents_title, documents_content


normalizer = Normalizer()


def preprocess_pipeline(content, configurations):
    str_empty = ' '
    stemmer = FindStems()
    tokenizer = Tokenizer()
    normalized = normalizer.normalize(content)
    result = tokenizer.tokenize_words(normalized)
    if configurations.get_config('do_stemming'):
        result = list(map(stemmer.convert_to_stem, result))
    if configurations.get_config('remove_stop_words'):
        result = StopWord(normal=False).clean(content)
    result = str_empty.join(content)
    return content


def heaps_law(dict_size, num_total_tokens, number):
    print(f'at {number}th document we seen {num_total_tokens} total tokens and dictionary size was {dict_size}')


def print_results(results):
    for single_result in results:
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


def save_index(configurations, pos_index):
    with open(f'../{configurations.get_config("dump_path")}/updated_pos_index.pkl', 'w') as file_to_write:
        pickle.dump(pos_index, file_to_write, pickle.HIGHEST_PROTOCOL)
        print(f'saved index with name updated_pos_index.pkl')


def load_index(configurations):
    index = None
    with open(f'../{configurations.get_config("dump_path")}/updated_pos_index.pkl', 'rb') as file_to_read:
        index = pickle.load(file_to_read)
    return index

# save_index(config)
# pos_index = load_index(config)
