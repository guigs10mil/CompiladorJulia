import sys
import parser

a = parser.Parser.run(sys.argv[1])

print(int(a))