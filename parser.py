import tokenizer
import prepro

class Parser:
    tokens = None
    
    @staticmethod
    def parseExpression():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = None

        if (Parser.tokens.position == -1):
            Parser.tokens.selectNext()

        if (Parser.tokens.actual.type == "INT"):
            res = Parser.parseTerm()

            while Parser.tokens.actual.type != "EOF":
                if (Parser.tokens.actual.type == "PLUS"):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == "INT"):
                        res += Parser.parseTerm()
                    else:
                        raise ValueError("soma")

                elif (Parser.tokens.actual.type == "MINUS"):
                    Parser.tokens.selectNext()
                    if (Parser.tokens.actual.type == "INT"):
                        res -= Parser.parseTerm()
                    else:
                        raise ValueError("subtracao")
                
                else:
                    raise ValueError("caracter invalido depois no INT")

            return res

        else:
            raise ValueError("o primeiro nao eh int, eh " + str(Parser.tokens.actual.type))

    @staticmethod
    def parseTerm():
        # consome os tokens do Tokenizer e analisa se a sintaxe está aderente à gramática proposta. retorna o resultado da expressão analisada

        res = int(Parser.tokens.actual.value)
        Parser.tokens.selectNext()

        while Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV":
            if (Parser.tokens.actual.type == "MULTI"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "INT"):
                    res *= int(Parser.tokens.actual.value)
                else:
                    raise ValueError("multiplicacao")

            elif (Parser.tokens.actual.type == "DIV"):
                Parser.tokens.selectNext()
                if (Parser.tokens.actual.type == "INT"):
                    res /= int(Parser.tokens.actual.value)
                else:
                    raise ValueError("divisao")
            
            else:
                raise ValueError("caracter invalido depois no INT")

            Parser.tokens.selectNext()

        return res

    @staticmethod
    def run(code):
        # recebe o código fonte como argumento, inicializa um objeto Tokenizador e retorna o resultado do parseExpression(). Esse método será chamado pelo main().

        Parser.tokens = tokenizer.Tokenizer(prepro.PrePro.filter(code))
        return Parser.parseExpression()