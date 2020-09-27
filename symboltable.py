class SymbolTable:
    def __init__(self):
        self.table = {}

    def getter(self, key):
        if key in self.table:
            return self.table[key]
        else:
            raise ValueError("Getter did not find the given variable: " + key)

    def setter(self, key, value):
        self.table[key] = value