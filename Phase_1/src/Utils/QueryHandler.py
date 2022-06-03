from Phase_1.src.Utils.PositionalIndex import pos_intersect
from Phase_1.src.Utils.utilities import preprocess_pipeline


class QueryHandler:
    def __init__(self, positional_index):
        self.positional_index = positional_index

    def answer_query(self, query):
        query = preprocess_query(query)
        not_queries = []
        and_queries = []
        empty_str = ' '
        is_not = False
        is_consecutive = False
        consecutive = []

        i = 0
        while i < len(query):
            next_occur = query.find(empty_str, i)
            substr = query[i:next_occur]
            if next_occur == -1:
                substr = query[i:]
            if substr == '_NOT_':
                is_not = True
                i = next_occur + 1
                continue
            elif is_not:
                not_queries.append(self.get_result([substr]))
                is_not = False
                i = next_occur + 1
                if next_occur == -1:
                    break
                continue
            elif substr[0] == '<':
                word = preprocess_pipeline(substr[1:])
                if word:
                    consecutive.append(word)
                i = next_occur + 1
                is_consecutive = True
                continue
            elif substr[-1] == '>':
                word = preprocess_pipeline(substr[:-1])
                if word:
                    consecutive.append(word)
                and_queries.append(self.get_result(consecutive))
                i = next_occur + 1
                consecutive.clear()
                is_consecutive = False
                if next_occur == -1:
                    break
                continue
            elif is_consecutive:
                consecutive.append(substr)
                i = next_occur + 1
                continue
            and_queries.append(self.get_result([substr]))
            i = next_occur + 1
            if next_occur == -1:
                break
        and_results = self.handle_queries(and_queries)
        not_results = self.handle_queries(not_queries)
        query_result = self.remove_by_sub_queries(and_results, not_results)
        get_score = lambda x: x['score']
        return sorted(query_result, key=get_score, reverse=True)

    def remove_by_sub_queries(self, in_results, out_results):
        answer = []
        for in_item_url in in_results:
            if in_item_url in out_results:
                continue
            index = {'title': self.positional_index.url_to_information[in_item_url]['title'],
                     'score': len(in_results[in_item_url]['positions']),
                     'url': in_item_url,
                     'content': self.positional_index.url_to_information[in_item_url]['content']}
            answer.append(index)
        return answer

    @staticmethod
    def handle_queries(queries):
        if not queries:
            return {}
        temporary_result = queries[0]
        for item_to_intersect in queries[1:]:
            if temporary_result:
                temporary_result = pos_intersect(temporary_result, item_to_intersect, 1000000)
            else:
                temporary_result = item_to_intersect
        return temporary_result

    def get_result(self, words):
        if words[0] not in self.positional_index.positional_index_structure:
            return {}
        temp_result = self.positional_index.positional_index_structure[words[0]]['indexes']
        for word in words[1:]:
            if word not in self.positional_index.positional_index_structure:
                temp_result = {}
                break
            indexes_of_word = self.positional_index.positional_index_structure[word]['indexes']
            if temp_result:
                temp_result = pos_intersect(temp_result, indexes_of_word, 1)
            else:
                temp_result = indexes_of_word
        return temp_result


def calc_string(string):
    state = False
    i = 0
    while i < len(string):
        ch = string[i]
        if ch == "\"":
            if state:
                string = string[:i] + '>' + string[i + 1:]
            else:
                string = string[:i] + '<' + string[i + 1:]
            state = 1 ^ state
        elif ch == '!':
            string = string[:i - 1] + ' _NOT_ ' + string[i + 1:]
        i += 1
    return string


def preprocess_query(query):
    query = calc_string(query)
    return preprocess_pipeline(query)
