import pytest
import re

from parser import Parser

from os import listdir
from os.path import isfile, join

mypath = "./tests/"
testfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

# Generate a test function structure based on the file name given
def functionShell(name: str):
    # get answer match
    ans = re.search("\\d+(?=.jl)", i)
    s = ""
    path = mypath + name

    # If the test should assert a print output
    if (name[4] == "_"):
        s = f"""def {name[:-3]}(capsys):
        code = open('{path}', 'r')
        Parser.run(code.read())
        captured = capsys.readouterr()
        assert captured.out == '{ans[0]}\\n' """

    # If the test should raise a ValueError
    elif (name[4:7] == "err"):
        s = f"""def {name[:-3]}():
        with pytest.raises(ValueError):
            code = open('{path}', 'r')
            Parser.run(code.read())"""
    return s


class TestClass:
    pass

for i in testfiles:
    # define function with functionShell info
    exec(functionShell(i))

    # Insert function as a TestClass method
    setattr(TestClass, "", globals()[i[:-3]])