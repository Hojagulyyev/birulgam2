class StoreNotFoundError(Exception):
    def __init__(self):
        super().__init__(f"store not found")


class StoreNameMustBeUniqueError(Exception):
    def __init__(self):
        super().__init__(f"store name must be unique")


class StoreCodeMustBeUniqueError(Exception):
    def __init__(self):
        super().__init__(f"store code must be unique")
