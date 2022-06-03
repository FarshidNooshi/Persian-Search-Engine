from Phase_1.src.Utils.utilities import preprocess_pipeline


class QueryHandler:
    def __init__(self, positional_index):
        self.positional_index = positional_index

    def answer_query(self, query):
        query = preprocess_pipeline(query)
        return query
