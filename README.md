# CompiladorJulia

![DiagramaSintatico](https://github.com/guigs10mil/CompiladorJulia/blob/master/DiagramaSintatico.png?raw=true)

### EBNF
EXPRESSION = TERM, {("+" | "-"), TERM} ;

TERM = FACTOR, {("*" | "/"), FACTOR} ;

FACTOR = NUMBER | (("+" | "-"), FACTOR) | ("(", EXPRESSION,")") ;

NUMBER = DIGIT, {DIGIT} ;

DIGIT = 0 | 1 | ... | 9 ;
