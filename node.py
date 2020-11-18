from symboltable import SymbolTable
from assembly import Assembly as asm

table = SymbolTable()

class Node:
    id = -1

    def __init__(self, value, children = None):
        self.value = value
        self.children = children
        self.id = Node.newId()

    def evaluate(self):
        pass

    @staticmethod
    def newId():
        Node.id += 1
        return Node.id

class BinOp(Node):
    def evaluate(self):
        child0 = self.children[0].evaluate()
        asm.write("PUSH EBX")
        child1 = self.children[1].evaluate()
        asm.write("POP EAX")

        # if (child0[0] == "String" or child1[0] == "String"):
        #     if self.value == "*":
        #         if child0[0] == "Bool":
        #             return ("String", str(child0[1]).lower() + str(child1[1]))
        #         if child1[0] == "Bool":
        #             return ("String", str(child0[1]) + str(child1[1]).lower())
                
        #         return ("String", str(child0[1]) + str(child1[1]))

        #     elif self.value == "==" and child0[0] == "String" and child1[0] == "String":
        #         return ("Bool", bool(child0[1] == child1[1]))

        #     else:
        #         raise ValueError("BinOp invalid string operation: " + str(child0[1]) + " " + self.value + " " + str(child1[1]))

        if self.value == "+":
            asm.write("ADD EAX, EBX")
            asm.write("MOV EBX, EAX")
            # return ("Int", int(child0[1] + child1[1]))
        if self.value == "-":
            asm.write("SUB EAX, EBX")
            asm.write("MOV EBX, EAX")
            # return ("Int", int(child0[1] - child1[1]))
        if self.value == "*":
            asm.write("IMUL EBX")
            asm.write("MOV EBX, EAX")
            # return ("Int", int(child0[1] * child1[1]))
        if self.value == "/":
            asm.write("DIV EBX")
            asm.write("MOV EBX, EAX")
            # return ("Int", int(child0[1] / child1[1]))
        if self.value == "&&":
            return ("Bool", bool(child0[1] and child1[1]))
        if self.value == "||":
            return ("Bool", bool(child0[1] or child1[1]))
        if self.value == "==":
            asm.write("CMP EAX, EBX")
            asm.write("CALL binop_je")
            # return ("Bool", bool(child0[1] == child1[1]))
        if self.value == ">":
            asm.write("CMP EAX, EBX")
            asm.write("CALL binop_jg")
            # return ("Bool", bool(child0[1] > child1[1]))
        if self.value == "<":
            asm.write("CMP EAX, EBX")
            asm.write("CALL binop_jl")
            # return ("Bool", bool(child0[1] < child1[1]))

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
        pos = table.getPosition(self.value) * 4 + 4
        asm.write(f"MOV EBX, [EBP-{pos}]")
        # return table.getter(self.value)

class Assignment(Node):
    def evaluate(self):
        if not table.hasIdentifier(self.children[0].value):
            asm.write("PUSH DWORD 0")

        # table.setter(self.children[0].value, self.children[1].evaluate())
        self.children[1].evaluate()
        table.setter(self.children[0].value)
        pos = table.getPosition(self.children[0].value) * 4 + 4
        asm.write(f"MOV [EBP-{pos}], EBX")
        asm.write("")
        
class Statment(Node):
    def evaluate(self):
        for i in self.children:
            i.evaluate()

class Print(Node):
    def evaluate(self):
        self.children[0].evaluate()
        asm.write("PUSH EBX")
        asm.write("CALL print")
        asm.write("POP EBX")

        # print(res)

class Readline(Node):
    def evaluate(self):
        return ("Int", int(input()))

class While(Node):
    def evaluate(self):
        asm.write(f"LOOP_{self.id}:")
        self.children[0].evaluate()
        asm.write(f"CMP EBX, False")
        asm.write(f"JE EXIT_{self.id}")
        asm.write("")
        self.children[1].evaluate()
        asm.write(f"JMP LOOP_{self.id}:")
        asm.write(f"EXIT_{self.id}:")
        asm.write("")

        # while self.children[0].evaluate()[1]:
        #     self.children[1].evaluate()

class If(Node):
    def evaluate(self):
        self.children[0].evaluate()
        asm.write(f"CMP EBX, False")
        asm.write(f"JE EXIT_{self.id}")
        self.children[1].evaluate()
        asm.write(f"EXIT_{self.id}:")

        # if self.children[0].evaluate()[1]:
        #     return self.children[1].evaluate()
        # else:
        if len(self.children) > 2:
            # return self.children[2].evaluate()
            self.children[0].evaluate()
            asm.write(f"CMP EBX, False")
            asm.write(f"JNE EXIT_ELSE_{self.id}")
            self.children[2].evaluate()
            asm.write(f"EXIT_ELSE_{self.id}:")

class Else(Node):
    def evaluate(self):
        return self.children[0].evaluate()

class IntVal(Node):
    def evaluate(self):
        asm.write(f"MOV EBX, {self.value}")
        # return ("Int", self.value)

class BoolVal(Node):
    def evaluate(self):
        if self.value:
            asm.write("CALL binop_true")
        else:
            asm.write("CALL binop_false")
        # return ("Bool", self.value)

class StrVal(Node):
    def evaluate(self):
        return ("String", self.value)

class NoOp(Node):
    def evaluate(self) -> int:
        return 0