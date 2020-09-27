from tokenMaker import Token

class Tokenizer:
    def __init__(self, origin):
        self.origin = origin
        self.position = -1
        self.actual = None
        self.operators = "+-*/()"
        self.operatorTypes = ["PLUS", "MINUS", "MULTI", "DIV", "POPEN", "PCLOSE"]
        self.names = ["println"]
        self.namesTypes = ["PRINT"]
    
    def selectNext(self):
        # lê o próximo token e atualiza o atributo atual

        if (self.position) + 1 >= len(self.origin):
            self.actual = Token("EOF", "")
            return

        self.position += 1
        tk = self.origin[self.position]

        while tk == " ":
            if (self.position) + 1 >= len(self.origin):
                self.actual = Token("EOF", "")
                return
            self.position += 1
            tk = self.origin[self.position]

        if (self.operators.find(tk) != -1):
            self.actual = Token(
                self.operatorTypes[self.operators.find(tk)],
                tk)
            return

        elif (tk == "="):
            self.actual = Token("EQUAL", tk)
            return

        elif (tk == "\n"):
            self.actual = Token("LBREAK", tk)
            return

        elif (tk.isnumeric()):
            while (len(self.origin) > self.position + 1 and self.origin[self.position + 1].isnumeric()):
                tk += self.origin[self.position + 1]
                self.position += 1

            self.actual = Token("INT", tk)
            return

        elif (tk.isalpha()):
            while (len(self.origin) > self.position + 1 and (self.origin[self.position + 1].isnumeric() or self.origin[self.position + 1].isalpha())):
                tk += self.origin[self.position + 1]
                self.position += 1

            if (tk not in self.names):
                self.actual = Token("IDENT", tk)
                return

            i = self.names.index(tk)
            self.actual = Token(self.namesTypes[i], tk)
            return
            

        
        else:
            raise ValueError("Invalid token")

