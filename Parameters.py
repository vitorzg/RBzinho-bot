class Parameters :
    def __init__(self, apikey, **kwargs):
        self.api_key = apikey;
        self.params = kwargs;
        
    def to_query(self):
        return {"api_key": self.api_key, **self.params}
