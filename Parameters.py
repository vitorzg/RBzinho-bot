class Parameters :
    def __init__(self, apikey, **kwargs):
        self.api_key = apikey;
        self.params = kwargs;
        
    def to_query(self):
        return {"api_key": self.api_key, **self.params}
    
    def add_group(self, group_name, **kwargs):
        for key, value in kwargs.items():
            self.params[f"{group_name}[{key}]"] = value