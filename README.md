# CompiladorJulia

![DiagramaSintatico](https://github.com/guigs10mil/CompiladorJulia/blob/master/DiagramaSintatico.png?raw=true)

### EBNF
BLOCK = { COMMAND } ;

COMMAND = (IDENTIFIER, "=", EXPRESSION, "\n") | ("println", "(", EXPRESSION, ")", "\n") | "\n" ;

EXPRESSION = TERM, {("+" | "-"), TERM} ;

TERM = FACTOR, {("*" | "/"), FACTOR} ;

FACTOR = NUMBER | (("+" | "-"), FACTOR) | ("(", EXPRESSION, ")") | IDENTIFIER ;

IDENTIFIER = CHARACTER, { CHARACTER | DIGIT | "_" } ;

CHARACTER = "a" | ... | "z" | "A" | ... | "Z" ;

NUMBER = DIGIT, {DIGIT} ;

DIGIT = "0" | "1" | ... | "9" ;
