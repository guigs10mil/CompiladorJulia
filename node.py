class Node:
    def __init__(self, value, children = None):
        self.value = value
        self.children = children

    def evaluate(self) -> int:
        return 0

class BinOp(Node):
    def evaluate(self) -> int:
        if self.value == "+":
            return self.children[0].evaluate() + self.children[1].evaluate()
        if self.value == "-":
            return self.children[0].evaluate() - self.children[1].evaluate()
        if self.value == "*":
            return self.children[0].evaluate() * self.children[1].evaluate()
        if self.value == "/":
            return self.children[0].evaluate() / self.children[1].evaluate()

class UnOp(Node):
    def evaluate(self) -> int:
        if self.value == "+":
            return self.children[0].evaluate()
        if self.value == "-":
            return -self.children[0].evaluate()

class IntVal(Node):
    def evaluate(self) -> int:
        return self.value

class NoOp(Node):
    def evaluate(self) -> int:
        return 0








# BinOp - Binary Operation. Contem 2 filhos 
# UnOp - Unary Operation. Contem um filho 
# IntVal - Integer value. Não contem filhos 
# NoOp - No Operation (Dummy). Não contem filhos