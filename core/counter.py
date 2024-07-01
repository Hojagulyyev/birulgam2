class Counter:
    '''
    Counter is used for rapid development.
    E.g.: writing sql stmts (queries) and etc. 
    '''
   
    def __init__(
        self,
        initial_value: int = 0,
    ):
        self.initial_value = initial_value
        self.value = initial_value

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.reset()

    def reset(self):
       self.value = self.initial_value

    def auto(self):
        self.value += 1
        return self.value - 1

    def start(self):
       self.reset()
       self.value += 1
       return self.value - 1
  