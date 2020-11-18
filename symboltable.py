class SymbolTable:
    def __init__(self):
        # self.table = {}
        self.keys = []

    # def getter(self, key):
    #     if key in self.table:
    #         return self.table[key]
    #     else:
    #         raise ValueError("Getter did not find the given variable: " + key)

    def hasIdentifier(self, key):
        return key in self.keys

    def getPosition(self, key):
        if key in self.keys:
            return self.keys.index(key)
        return None

    # def setter(self, key, value):
    #     if key in self.table:
    #         if value[0] != self.table[key][0]:
    #             raise ValueError("Variable type does not match the Symbol Table: " + value[0] + " != " + self.table[key][0])
    #     else :
    #         self.keys.append(key)

    #     self.table[key] = value
    
    def setter(self, key):
        if key in self.keys:
            return
        self.keys.append(key)
