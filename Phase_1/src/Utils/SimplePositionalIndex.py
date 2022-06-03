from matplotlib import pyplot as plt

from Phase_1.src.Utils.StopWord import Document
from Phase_1.src.Utils.utilities import preprocess_pipeline, heaps_law


class SimplePositionalIndex:
    def __init__(self, documents_url, documents_title, documents_content, show=True):
        self.Documents = [Document(documents_content[i], documents_url[i], documents_title[i]) for i in
                          range(len(documents_url))]
        self.positional_index_structure = {}
        self.url_to_information = {}
        self.show = show
        self.build_positional_index()
        self.build_url_to_information_dict()

    def build_positional_index(self):
        num_tokens = 0
        x = []
        y = []
        for i, document in enumerate(self.Documents):
            preprocessed_content = preprocess_pipeline(document.content)
            processed_content = process_positions(preprocessed_content)
            title_of_document = document.title
            url = document.url
            num_tokens += len(processed_content.keys())
            for word, positions in processed_content.items():
                self.add_index(word, positions, title_of_document, url)
            if i % 500 or not i or i > 2000:
                continue
            x.append(len(self.positional_index_structure.keys()))
            y.append(num_tokens)
            if self.show:
                heaps_law(dict_size=len(self.positional_index_structure.keys()), num_total_tokens=num_tokens, number=i)
        if self.show:
            heaps_law(dict_size=len(self.positional_index_structure.keys()), num_total_tokens=num_tokens,
                      number=len(self.Documents))
            plt.clf()
            plt.title('With Stemming')
            plt.plot(x, y, 'g-')
            plt.show()

    def add_index(self, word, positions, title, url):
        index_to_add = generate_index(positions, title)
        if word not in self.positional_index_structure:
            self.positional_index_structure[word] = {"total occurrences": 0,
                                                     "indexes": {}}
        self.positional_index_structure[word]["total occurrences"] += index_to_add[
            "number of occurrences in document"]
        self.positional_index_structure[word]["indexes"][url] = index_to_add

    def build_url_to_information_dict(self):
        for document in self.Documents:
            self.url_to_information[document.url] = {"title": document.title,
                                                     "content": document.content}


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


def docID(number, lst_urls):
    return lst_urls[number]


def position(plist):
    return plist['positions']


def pos_intersect(p1, p2, k):
    answer = {}  # answer <- ()
    len1 = len(p1)
    len2 = len(p2)
    i = j = 0
    lst_urls1 = sorted(list(p1.keys()))
    lst_urls2 = sorted(list(p2.keys()))
    while i != len1 and j != len2:
        key = docID(i, lst_urls1)
        key2 = docID(j, lst_urls2)
        if key == key2:
            l = []
            pp1 = position(p1[key])
            pp2 = position(p2[key])

            plen1 = len(pp1)
            plen2 = len(pp2)
            ii = jj = 0
            while ii != plen1:
                while jj != plen2:
                    if abs(pp1[ii] - pp2[jj]) <= k:
                        l.append(pp2[jj])
                    elif pp2[jj] > pp1[ii]:
                        break
                    jj += 1
                # l.sort()
                while l != [] and abs(l[0] - pp1[ii]) > k:
                    l.remove(l[0])
                for ps in l:
                    if key in answer:
                        # answer[key]['positions'].extend([pp1[ii], ps])
                        answer[key]['positions'].extend([max(pp1[ii], ps)])
                    else:
                        answer[key] = {'positions': [max(pp1[ii], ps)]}
                ii += 1
            i += 1
            j += 1
            if key in answer:
                answer[key]['positions'] = list(set(answer[key]['positions']))
        elif key < key2:
            i += 1
        else:
            j += 1
    return answer
