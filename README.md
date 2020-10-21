# CompiladorJulia

![DiagramaSintatico](https://github.com/guigs10mil/CompiladorJulia/blob/master/DiagramaSintatico.png?raw=true)

### EBNF
BLOCK = { COMMAND } ;

COMMAND = ( ASSIGNMENT | PRINT | WHILE | IF ), "\n" | "\n" ;

ASSIGNMENT = IDENTIFIER, "=", ( REL_EXPRESSION | "readline", "(", ")" ) ;

PRINT = "println", "(", REL_EXPRESSION, ")" ;

WHILE = "while", REL_EXPRESSION, "\n", BLOCK, "end" ;

IF = "if", REL_EXPRESSION, "\n", BLOCK, { ELSEIF }, [ ELSE ], "end" ;

ELSEIF = "elseif", REL_EXPRESSION, "\n", BLOCK ;

ELSE = "else", "\n", BLOCK ;

REL_EXPRESSION = EXPRESSION, { ( "==" | ">" | "<" ), EXPRESION } ;

EXPRESSION = TERM, { ( "+" | "-" | "||" ), TERM } ;

TERM = FACTOR, { ( "*" | "/" | "&&" ), FACTOR } ;

FACTOR = NUMBER | ( ( "+" | "-" | "!" ), FACTOR ) | ( "(", REL_EXPRESSION, ")" ) | IDENTIFIER ;

IDENTIFIER = CHARACTER, { CHARACTER | DIGIT | "_" } ;

CHARACTER = "a" | ... | "z" | "A" | ... | "Z" ;

NUMBER = DIGIT, { DIGIT } ;

DIGIT = "0" | "1" | ... | "9" ;
