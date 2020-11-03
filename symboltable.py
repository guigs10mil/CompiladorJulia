class SymbolTable:
    def __init__(self):
        self.table = {}

    def getter(self, key):
        if key in self.table:
            return self.table[key]
        else:
            raise ValueError("Getter did not find the given variable: " + key)

    def setter(self, key, value):
        if key in self.table:
            if value[0] != self.table[key][0]:
                raise ValueError("Variable type does not match the Symbol Table: " + value[0] + " != " + self.table[key][0])
        self.table[key] = value