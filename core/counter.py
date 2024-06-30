class Counter:
    '''
    Counter is used for rapid development.
    E.g.: writing sql stmts (queries) and etc. 
    '''
   
    def __init__(
        self,
        value: int = 0,
    ):
        self.value = value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.reset()

    def reset(self):
       self.value = 0

    def auto(self):
        self.value += 1
        return self.value - 1

    def start(self, value):
       self.value = value + 1
       return self.value - 1
    
    def end(self):
        value = self.value
        self.reset()
        return value
