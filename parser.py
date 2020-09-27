from tokenizer import Tokenizer
import prepro
from node import *

class Parser:
    tokens: Tokenizer = None

    @staticmethod
    def parseBlock():
        res = Statment("Block", [])

        if (Parser.tokens.position == -1):
            Parser.tokens.selectNext()

        while Parser.tokens.actual.type != "EOF":
            res.children.append(Parser.parseCommand())

        return res

    @staticmethod
    def parseCommand():

        res = None

        if (Parser.tokens.actual.type == "IDENT"):
            identifier = Parser.tokens.actual
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.type == "EQUAL"):
                Parser.tokens.selectNext()
                res = Assignment("=", [identifier, Parser.parseExpression()])
            
            else:
                raise ValueError("Invalid token after identifier: " + Parser.tokens.actual.type)

            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("No line break found. Found " + Parser.tokens.actual.type + " instead.")
            

        elif (Parser.tokens.actual.type == "PRINT"):
            Parser.tokens.selectNext()
            if (Parser.tokens.actual.type == "POPEN"):
                Parser.tokens.selectNext()
                # res = Parser.parseExpression()
                res = Print("println", [Parser.parseExpression()])
                if (Parser.tokens.actual.type == "PCLOSE"):
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("Closing parenteses not found")
            
            else:
                raise ValueError("Invalid token in PRINT: " + Parser.tokens.actual.type)
                
            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("No line break found. Found " + Parser.tokens.actual.type + " instead.")
        
        elif (Parser.tokens.actual.type == "LBREAK"):
            Parser.tokens.selectNext()
            res = NoOp("NoOp")
            return res

        else:
            raise ValueError("Invalid token in parse command: " + Parser.tokens.actual.type)

        

    
    @staticmethod
    def parseExpression():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = Parser.parseTerm()

        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
            if (Parser.tokens.actual.type == "PLUS"):
                Parser.tokens.selectNext()
                res = BinOp("+", [res, Parser.parseTerm()])

            elif (Parser.tokens.actual.type == "MINUS"):
                Parser.tokens.selectNext()
                res = BinOp("-", [res, Parser.parseTerm()])

        return res

    @staticmethod
    def parseTerm():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = Parser.parseFactor()

        while Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV":
            if (Parser.tokens.actual.type == "MULTI"):
                Parser.tokens.selectNext()
                res = BinOp("*", [res, Parser.parseFactor()])

            elif (Parser.tokens.actual.type == "DIV"):
                Parser.tokens.selectNext()
                res = BinOp("/", [res, Parser.parseFactor()])

        return res

    @staticmethod
    def parseFactor():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = None

        if (Parser.tokens.actual.type == "INT"):
            res = IntVal(int(Parser.tokens.actual.value))
            Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == "PLUS"):
            Parser.tokens.selectNext()
            res = UnOp("+", [Parser.parseFactor()])

        elif (Parser.tokens.actual.type == "MINUS"):
            Parser.tokens.selectNext()
            res = UnOp("-", [Parser.parseFactor()])

        elif (Parser.tokens.actual.type == "IDENT"):
            res = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == "POPEN"):
            Parser.tokens.selectNext()
            res = Parser.parseExpression()
            if (Parser.tokens.actual.type == "PCLOSE"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("Closing parenteses not found")
        
        else:
            raise ValueError("Invalid token in FACTOR: " + Parser.tokens.actual.type)

        return res

    @staticmethod
    def run(code):
        # recebe o código fonte como argumento, inicializa um objeto Tokenizador e retorna o resultado do parseExpression(). Esse método será chamado pelo main().

        Parser.tokens = Tokenizer(prepro.PrePro.filter(code))
        res = Parser.parseBlock()

        # if Parser.tokens.actual.type != "EOF":
        #     raise ValueError("Program ended before EOF. Current type is " + Parser.tokens.actual.type + ".")

        return res.evaluate()