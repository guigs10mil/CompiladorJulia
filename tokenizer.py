import token

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = -1
        self.actual = None
        self.operators = "+-*/()"
        self.operatorTypes = ["PLUS", "MINUS", "MULTI", "DIV", "POPEN", "PCLOSE"]
    
    def selectNext(self):
        # lê o próximo token e atualiza o atributo atual

        if (self.position) + 1 >= len(self.origin):
            self.actual = token.Token("EOF", "")
            return

        self.position += 1
        tk = self.origin[self.position]

        while tk == " ":
            if (self.position) + 1 >= len(self.origin):
                self.actual = token.Token("EOF", "")
                return
            self.position += 1
            tk = self.origin[self.position]

        if (self.operators.find(tk) != -1):
            self.actual = token.Token(
                self.operatorTypes[self.operators.find(tk)],
                tk)
            return

        if (tk.isnumeric()):
            while (len(self.origin) > self.position + 1 and self.origin[self.position + 1].isnumeric()):
                tk += self.origin[self.position + 1]
                self.position += 1

            self.actual = token.Token("INT", tk)
            return


