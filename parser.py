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

        while (Parser.tokens.actual.type != "EOF"
                and Parser.tokens.actual.type != "ELSEIF"
                and Parser.tokens.actual.type != "ELSE"
                and Parser.tokens.actual.type != "END"):
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
                if (Parser.tokens.actual.type == "READLINE"):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == "POPEN"):
                        Parser.tokens.selectNext()
                        if (Parser.tokens.actual.type == "PCLOSE"):
                            Parser.tokens.selectNext()
                        else:
                            raise ValueError("Closing parenteses not found. Found " + Parser.tokens.actual.type + " instead.")
                    else:
                        raise ValueError("Opening parenteses not found. Found " + Parser.tokens.actual.type + " instead.")

                    res = Assignment("=", [identifier, Readline(None)])
                
                else:
                    res = Assignment("=", [identifier, Parser.parseRelExpression()])
            
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
                res = Print("println", [Parser.parseRelExpression()])
                if (Parser.tokens.actual.type == "PCLOSE"):
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("Closing parenteses not found. Found " + Parser.tokens.actual.type + " instead.")
            
            else:
                raise ValueError("Invalid token in PRINT: " + Parser.tokens.actual.type)
                
            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("No line break found. Found " + Parser.tokens.actual.type + " instead.")

        elif (Parser.tokens.actual.type == "WHILE"):
            Parser.tokens.selectNext()
            res = While("while", [Parser.parseRelExpression()])

            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("No line break found after while. Found " + Parser.tokens.actual.type + " instead.")

            res.children.append(Parser.parseBlock())

            if (Parser.tokens.actual.type == "END"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("No end of while found. Found " + Parser.tokens.actual.type + " instead.")
                
            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
                return res
            else:
                raise ValueError("No line break found. Found " + Parser.tokens.actual.type + " instead.")
        
        elif (Parser.tokens.actual.type == "IF"):
            Parser.tokens.selectNext()
            res = If("if", [Parser.parseRelExpression()])

            previousIf = res

            if (Parser.tokens.actual.type == "LBREAK"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("No line break found after if. Found " + Parser.tokens.actual.type + " instead.")

            res.children.append(Parser.parseBlock())

            while (Parser.tokens.actual.type == "ELSEIF"):
                Parser.tokens.selectNext()
                tmpIf = If("if", [Parser.parseRelExpression()])
                
                previousIf.children.append(tmpIf)
                previousIf = tmpIf

                if (Parser.tokens.actual.type == "LBREAK"):
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("No line break found after elseif. Found " + Parser.tokens.actual.type + " instead.")

                previousIf.children.append(Parser.parseBlock())

            if (Parser.tokens.actual.type == "ELSE"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "LBREAK"):
                    Parser.tokens.selectNext()
                else:
                    raise ValueError("No line break found after else. Found " + Parser.tokens.actual.type + " instead.")

                previousIf.children.append(Parser.parseBlock())


            if (Parser.tokens.actual.type == "END"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("No end of if found. Found " + Parser.tokens.actual.type + " instead.")
                
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
    def parseRelExpression():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = Parser.parseExpression()

        while Parser.tokens.actual.type == "EQUALS" or Parser.tokens.actual.type == "GREATER" or Parser.tokens.actual.type == "LESSTHAN":
            if (Parser.tokens.actual.type == "EQUALS"):
                Parser.tokens.selectNext()
                res = BinOp("==", [res, Parser.parseExpression()])

            elif (Parser.tokens.actual.type == "GREATER"):
                Parser.tokens.selectNext()
                res = BinOp(">", [res, Parser.parseExpression()])

            elif (Parser.tokens.actual.type == "LESSTHAN"):
                Parser.tokens.selectNext()
                res = BinOp("<", [res, Parser.parseExpression()])

        return res
    
    @staticmethod
    def parseExpression():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = Parser.parseTerm()

        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "OR":
            if (Parser.tokens.actual.type == "PLUS"):
                Parser.tokens.selectNext()
                res = BinOp("+", [res, Parser.parseTerm()])

            elif (Parser.tokens.actual.type == "MINUS"):
                Parser.tokens.selectNext()
                res = BinOp("-", [res, Parser.parseTerm()])

            elif (Parser.tokens.actual.type == "OR"):
                Parser.tokens.selectNext()
                res = BinOp("||", [res, Parser.parseTerm()])

        return res

    @staticmethod
    def parseTerm():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = Parser.parseFactor()

        while Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "AND":
            if (Parser.tokens.actual.type == "MULTI"):
                Parser.tokens.selectNext()
                res = BinOp("*", [res, Parser.parseFactor()])

            elif (Parser.tokens.actual.type == "DIV"):
                Parser.tokens.selectNext()
                res = BinOp("/", [res, Parser.parseFactor()])

            elif (Parser.tokens.actual.type == "AND"):
                Parser.tokens.selectNext()
                res = BinOp("&&", [res, Parser.parseFactor()])

        return res

    @staticmethod
    def parseFactor():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = None

        if (Parser.tokens.actual.type == "INT"):
            res = IntVal(int(Parser.tokens.actual.value))
            Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == "NOT"):
            Parser.tokens.selectNext()
            res = UnOp("!", [Parser.parseFactor()])

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
            res = Parser.parseRelExpression()
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

        return res.evaluate()