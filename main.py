import sys
import parser

code = open(sys.argv[1], "r")

a = parser.Parser.run(code.read())

print(int(a))