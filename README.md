# CompiladorJulia

![DiagramaSintatico](https://github.com/guigs10mil/CompiladorJulia/blob/master/DiagramaSintatico.png?raw=true)

### EBNF
PROGRAM = { COMMAND | FUNCTION } ;

BLOCK = { COMMAND } ;

COMMAND = ( ASSIGNMENT | PRINT | WHILE | IF | LOCAL | RETURN | FUNCALL ), "\n" | "\n" ;

FUNCTION = "function", IDENTIFIER, "(", [ IDENTIFIER, "::", "TYPE", { ",", IDENTIFIER, "::", "TYPE" } ], ")", "::", TYPE, "\n", BLOCK, "end" ;

LOCAL = "local", IDENTIFIER, "::", "TYPE" ;

ASSIGNMENT = IDENTIFIER, "=", ( REL_EXPRESSION | "readline", "(", ")" ) ;

PRINT = "println", "(", REL_EXPRESSION, ")" ;

WHILE = "while", REL_EXPRESSION, "\n", BLOCK, "end" ;

IF = "if", REL_EXPRESSION, "\n", BLOCK, { ELSEIF }, [ ELSE ], "end" ;

ELSEIF = "elseif", REL_EXPRESSION, "\n", BLOCK ;

ELSE = "else", "\n", BLOCK ;

RETURN = "return", REL_EXPRESSION ;

REL_EXPRESSION = EXPRESSION, { ( "==" | ">" | "<" ), EXPRESION } ;

EXPRESSION = TERM, { ( "+" | "-" | "||" ), TERM } ;

TERM = FACTOR, { ( "*" | "/" | "&&" ), FACTOR } ;

FACTOR = NUMBER | BOOLEAN | STRING | ( ( "+" | "-" | "!" ), FACTOR ) | ( "(", REL_EXPRESSION, ")" ) | IDENTIFIER | FUNCALL ;

FUNCALL = IDENTIFIER, "(", [ REL_EXPRESSION, { ",", REL_EXPRESSION } ] , ")" ;

TYPE = "Int", "Bool", "String" ;

BOOLEAN = "true" | "false" ;

STRING = "'", {.*?}, "'" ;

IDENTIFIER = CHARACTER, { CHARACTER | DIGIT | "_" } ;

CHARACTER = "a" | ... | "z" | "A" | ... | "Z" ;

NUMBER = DIGIT, { DIGIT } ;

DIGIT = "0" | "1" | ... | "9" ;
