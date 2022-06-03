class Config:
    def __init__(self):
        self.config = {
            'champions_list': False,
            'champions_list_size': 20,
            'documents_to_show': 5
        }

    def get_config(self, config_name):
        return self.config[config_name]
