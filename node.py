from symboltable import SymbolTable

table = SymbolTable()

class Node:
    def __init__(self, value, children = None):
        self.value = value
        self.children = children

    def evaluate(self) -> int:
        return 0

class BinOp(Node):
    def evaluate(self):
        child0 = self.children[0].evaluate()
        child1 = self.children[1].evaluate()

        if (child0[0] == "String" or child1[0] == "String"):
            if self.value == "*":
                if child0[0] == "Bool":
                    return ("String", str(child0[1]).lower() + str(child1[1]))
                if child1[0] == "Bool":
                    return ("String", str(child0[1]) + str(child1[1]).lower())
                
                return ("String", str(child0[1]) + str(child1[1]))

            elif self.value == "==" and child0[0] == "String" and child1[0] == "String":
                return ("Bool", bool(child0[1] == child1[1]))

            else:
                raise ValueError("BinOp invalid string operation: " + str(child0[1]) + " " + self.value + " " + str(child1[1]))

        if self.value == "+":
            return ("Int", int(child0[1] + child1[1]))
        if self.value == "-":
            return ("Int", int(child0[1] - child1[1]))
        if self.value == "*":
            return ("Int", int(child0[1] * child1[1]))
        if self.value == "/":
            return ("Int", int(child0[1] / child1[1]))
        if self.value == "&&":
            return ("Bool", bool(child0[1] and child1[1]))
        if self.value == "||":
            return ("Bool", bool(child0[1] or child1[1]))
        if self.value == "==":
            return ("Bool", bool(child0[1] == child1[1]))
        if self.value == ">":
            return ("Bool", bool(child0[1] > child1[1]))
        if self.value == "<":
            return ("Bool", bool(child0[1] < child1[1]))

class UnOp(Node):
    def evaluate(self):
        child0 = self.children[0].evaluate()

        if (child0[0] == "String"):
            raise ValueError("UnOp cannot work with strings: " + child0[1])

        if self.value == "+":
            return child0
        if self.value == "-":
            return ("Int", -child0[1])
        if self.value == "!":
            return ("Bool", bool(not child0[1]))

class Identifier(Node):
    def evaluate(self):
        return table.getter(self.value)

class Assignment(Node):
    def evaluate(self):
        table.setter(self.children[0].value, self.children[1].evaluate())
        
class Statment(Node):
    def evaluate(self):
        for i in self.children:
            i.evaluate()

class Print(Node):
    def evaluate(self):
        print(self.children[0].evaluate()[1])

class Readline(Node):
    def evaluate(self):
        return ("Int", int(input()))

class While(Node):
    def evaluate(self):
        while self.children[0].evaluate()[1]:
            self.children[1].evaluate()

class If(Node):
    def evaluate(self):
        if self.children[0].evaluate()[1]:
            return self.children[1].evaluate()
        else:
            if len(self.children) > 2:
                return self.children[2].evaluate()

class Else(Node):
    def evaluate(self):
        return self.children[0].evaluate()

class IntVal(Node):
    def evaluate(self):
        return ("Int", self.value)

class BoolVal(Node):
    def evaluate(self):
        return ("Bool", self.value)

class StrVal(Node):
    def evaluate(self):
        return ("String", self.value)

class NoOp(Node):
    def evaluate(self) -> int:
        return 0