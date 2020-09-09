import tokenizer
import prepro

class Parser:
    tokens = None
    
    @staticmethod
    def parseExpression():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        if (Parser.tokens.position == -1):
            Parser.tokens.selectNext()

        res = Parser.parseTerm()

        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
            if (Parser.tokens.actual.type == "PLUS"):
                Parser.tokens.selectNext()
                res += Parser.parseTerm()

            elif (Parser.tokens.actual.type == "MINUS"):
                Parser.tokens.selectNext()
                res -= Parser.parseTerm()

        return res

    @staticmethod
    def parseTerm():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = Parser.parseFactor()

        while Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV":
            if (Parser.tokens.actual.type == "MULTI"):
                Parser.tokens.selectNext()
                res *= Parser.parseFactor()

            elif (Parser.tokens.actual.type == "DIV"):
                Parser.tokens.selectNext()
                res /= Parser.parseFactor()

        return res

    @staticmethod
    def parseFactor():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        # res = int(Parser.tokens.actual.value)
        res = 0
        # Parser.tokens.selectNext()

        if (Parser.tokens.actual.type == "INT"):
            res = int(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif (Parser.tokens.actual.type == "PLUS"):
            Parser.tokens.selectNext()
            res = Parser.parseFactor()

        elif (Parser.tokens.actual.type == "MINUS"):
            Parser.tokens.selectNext()
            res = -Parser.parseFactor()

        elif (Parser.tokens.actual.type == "POPEN"):
            Parser.tokens.selectNext()
            res = Parser.parseExpression()
            if (Parser.tokens.actual.type == "PCLOSE"):
                Parser.tokens.selectNext()
            else:
                raise ValueError("Closing parenteses not found")
        
        else:
            raise ValueError("caracter invalido no Factor")

        return res

    @staticmethod
    def run(code):
        # recebe o código fonte como argumento, inicializa um objeto Tokenizador e retorna o resultado do parseExpression(). Esse método será chamado pelo main().

        Parser.tokens = tokenizer.Tokenizer(prepro.PrePro.filter(code))
        res = Parser.parseExpression()

        if Parser.tokens.actual.type != "EOF":
            raise ValueError("Program ended before EOF. Current type is " + Parser.tokens.actual.type + ".")

        return res