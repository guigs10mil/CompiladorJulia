# CompiladorJulia

![diagramaSintatico](https://github.com/guigs10mil/CompiladorJulia/blob/master/diagramaSintatico.png?raw=true)

### EBNF
EXPRESSION = TERM, {("+" | "-"), TERM} ;

TERM = NUMBER, {("*" | "/"), NUMBER} ;
NUMBER = DIGIT, {DIGIT} ;
DIGIT = 0 | 1 | ... | 9 ;