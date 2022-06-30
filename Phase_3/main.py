from hazm import *
#
def calc_string(string):
    print(string)
    state = False
    i = 0
    while i < len(string):
        ch = string[i]
        if ch == "\"":
            if state:
                string = string[:i] + ')' + string[i + 1:]
            else:
                string = string[:i] + '(' + string[i + 1:]
            state = 1 ^ state
        i += 1
    string = str.replace(string, ' ! ', 'NOT')
    string = str.replace(string, ' + ', 'AND')
    string = str.replace(string, ' ', 'OR')
    state = False
    i = 0
    while i < len(string):
        ch = string[i]
        if ch == "(":
            state = True
        elif ch == ')':
            state = False
        if state and ch == 'O':
            string = string[:i] + ' ' + string[i + 2:]
        i += 1
    string = str.replace(string, 'NOT', ' NOT ')
    string = str.replace(string, 'AND', ' AND ')
    string = str.replace(string, 'OR', ' OR ')
    return string

# normalizer = Normalizer()
#
# def preprocess_pipeline(query):
#     str_empty = ' '
#     stemmer = Stemmer()
#     query = normalizer.normalize(query)
#     query = word_tokenize(query)
#     query = StopWord(normal=False).clean(query)
#     query = [stemmer.stem(word) for word in query]
#     query = str_empty.join(query)
#     return query


def preprocess_query(query):
    query = calc_string(query)
    return query


# def query_data(query):
#     query_to_ask_es = preprocess_query(query)
#     res = es.search(index="ir-news-index", body={"query": {"query_string": {"fields": ["content"],
#                                                                             "query": query_to_ask_es
#                                                                             }}})
#     return res


print(preprocess_query('تحریم‌های آمریکا علیه "جمهوری اسلامی ایران" ! آلمان + انگلیس'))
