from symboltable import SymbolTable

table = SymbolTable()

class Node:
    def __init__(self, value, children = None):
        self.value = value
        self.children = children

    def evaluate(self) -> int:
        return 0

class BinOp(Node):
    def evaluate(self) -> int:
        if self.value == "+":
            return int(self.children[0].evaluate() + self.children[1].evaluate())
        if self.value == "-":
            return int(self.children[0].evaluate() - self.children[1].evaluate())
        if self.value == "*":
            return int(self.children[0].evaluate() * self.children[1].evaluate())
        if self.value == "/":
            return int(self.children[0].evaluate() / self.children[1].evaluate())
        if self.value == "&&":
            return bool(self.children[0].evaluate() and self.children[1].evaluate())
        if self.value == "||":
            return bool(self.children[0].evaluate() or self.children[1].evaluate())
        if self.value == "==":
            return bool(self.children[0].evaluate() == self.children[1].evaluate())
        if self.value == ">":
            return bool(self.children[0].evaluate() > self.children[1].evaluate())
        if self.value == "<":
            return bool(self.children[0].evaluate() < self.children[1].evaluate())

class UnOp(Node):
    def evaluate(self) -> int:
        if self.value == "+":
            return self.children[0].evaluate()
        if self.value == "-":
            return -self.children[0].evaluate()
        if self.value == "!":
            return bool(not self.children[0].evaluate())

class Identifier(Node):
    def evaluate(self) -> int:
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
        print(self.children[0].evaluate())

class Readline(Node):
    def evaluate(self):
        return int(input())

class While(Node):
    def evaluate(self):
        while self.children[0].evaluate():
            self.children[1].evaluate()

class If(Node):
    def evaluate(self):
        if self.children[0].evaluate():
            return self.children[1].evaluate()
        else:
            if len(self.children) > 2:
                return self.children[2].evaluate()

class Else(Node):
    def evaluate(self):
        return self.children[0].evaluate()

class IntVal(Node):
    def evaluate(self) -> int:
        return self.value

class NoOp(Node):
    def evaluate(self) -> int:
        return 0