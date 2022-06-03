class Config:
    def __init__(self):
        self.config = {
            'champions_list': False,
            'champions_list_size': 25,
            'documents_to_show': 10,
            'documents': [],
            'show_heaps_law': False,
            'show_zipf_law': False,
            'documents_path': 'Phase_1/assets/IR_data_news_12k.json',
        }

    def get_config(self, config_name):
        return self.config[config_name]

    def set_config(self, config_name, value):
        self.config[config_name] = value
