from abc import ABC, abstractmethod
from typing import List
from symbol_table import SymbolTable, LocalSymbolTable


class Node(ABC):
    def __init__(self, value, children: List):
        self.value = value
        self.children = children

    @abstractmethod
    def evaluate(self, symbolTable=None):
        pass


class NoOp(Node):
    def __init__(self, value=None, children: List[Node] = []):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable

        return None


class IntVal(Node):
    def __init__(self, value: int, children: List[Node] = []):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable

        return ("int", self.value)


class StringVal(Node):
    def __init__(self, value: str, children: List[Node] = []):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable

        return ("string", self.value)


class UnOp(Node):
    def __init__(self, value: str, children: List[Node]):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable

        if self.value == "+":
            return ("int", self.children[0].evaluate(self.symbolTable)[1])
        elif self.value == "-":
            return ("int", -self.children[0].evaluate(self.symbolTable)[1])
        elif self.value == "!":
            return ("int", int(not self.children[0].evaluate(self.symbolTable)[1]))


class BinOp(Node):
    def __init__(self, value: str, children: List[Node]):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable

        child0 = self.children[0].evaluate(self.symbolTable)
        child1 = self.children[1].evaluate(self.symbolTable)

        # Bin ops que podem ter filhos de tipos diferentes
        if self.value == ".":
            return ("string", str(child0[1]) + str(child1[1]))
        elif self.value == "==":
            return (child0[0], int(child0[1] == child1[1]))
        elif self.value == ">":
            return (child0[0], int(child0[1] > child1[1]))
        elif self.value == ">=":
            return (child0[0], int(child0[1] >= child1[1]))
        elif self.value == "<":
            return (child0[0], int(child0[1] < child1[1]))
        elif self.value == "<=":
            return (child0[0], int(child0[1] <= child1[1]))
        elif self.value == "&&":
            return (child0[0], int(child0[1] and child1[1]))
        elif self.value == "||":
            return (child0[0], int(child0[1] or child1[1]))

        # Bin ops que devem ter os dois filhos do mesmo tipo
        if child0[0] != child1[0]:
            raise Exception(
                f"Bin op with incompatible types {child0[0]} and {child1[0]}")
        if self.value == "+":
            return (child0[0], child0[1] + child1[1])
        elif self.value == "-":
            return (child0[0], child0[1] - child1[1])
        elif self.value == "*":
            return (child0[0], child0[1] * child1[1])
        elif self.value == "/":
            return (child0[0], child0[1] // child1[1])


class Identifier(Node):
    def __init__(self, value: str, children: List[Node] = []):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable

        return self.symbolTable.getter(self.value)


class Assignment(Node):
    def __init__(self, value: str, children: List[Node]):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable

        if self.children[0].value not in self.symbolTable.table.keys():
            # print(SymbolTable().table)
            raise Exception(f"Variable not declared {self.children[0].value} ")
        expression = self.children[1].evaluate(self.symbolTable)
        # Check if expression has the same type as the variable
        if self.symbolTable.table[self.children[0].value][0] != expression[0]:
            raise Exception("Overwriting variable with different type")
        return self.symbolTable.setter(self.children[0].value, expression)


class Println(Node):
    def __init__(self, value: str, children: List[Node]):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable

        print(self.children[0].evaluate(self.symbolTable)[1])


class Block(Node):
    def __init__(self, value: str = None, children: List[Node] = []):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable

        for child in self.children:
            try:
                child.evaluate(self.symbolTable)
            except ReturnException as e:
                return e.args[0]
        return None


class While(Node):
    def __init__(self, value: str = None, children: List[Node] = []):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable

        while self.children[0].evaluate(self.symbolTable)[1]:
            self.children[1].evaluate(self.symbolTable)


class If(Node):
    def __init__(self, value: str = None, children: List[Node] = []):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable

        if len(self.children) == 2:
            if self.children[0].evaluate(self.symbolTable)[1]:
                self.children[1].evaluate(self.symbolTable)
        else:
            if self.children[0].evaluate(self.symbolTable)[1]:
                self.children[1].evaluate(self.symbolTable)
            else:
                self.children[2].evaluate(self.symbolTable)


# class Readline(Node):
#     def __init__(self, value: str = None, children: List[Node] = []):
#         self.value = value
#         self.children = children

#     def evaluate(self, symbolTable=None):
#         if symbolTable is None:
#             self.symbolTable = SymbolTable()
#         else:
#             self.symbolTable = symbolTable

#         return ("int", int(input()))


class VarDec(Node):
    def __init__(self, value: str, children: List[Node]):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable
        if self.children[0].value in self.symbolTable.table.keys():
            raise Exception("Variable already declared")
        type = self.value
        if len(self.children) == 2:
            expression = self.children[1].evaluate(self.symbolTable)
            if expression[0] != type:
                raise Exception(
                    f"Invalid variable type on declaration of {self.value} {self.children[0].value} {self.children[1].value} \
                    \n Expected {type} but got {expression[0]}")
            self.symbolTable.setter(
                self.children[0].value, expression)
            return None

        if self.value == "int":
            self.symbolTable.setter(self.children[0].value, ("int", 0))

        elif self.value == "string":
            self.symbolTable.setter(self.children[0].value, ("string", ""))
        else:
            raise Exception("Invalid variable type")

        return None


class FuncDec(Node):
    def __init__(self, value: str, children: List[Node]):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            self.symbolTable = SymbolTable()
        else:
            self.symbolTable = symbolTable
        # print(f"{self.value} {self}")
        # print(self.children)
        self.symbolTable.setter(self.children[0].value, ("Function", self))


class FuncCall(Node):
    def __init__(self, value, children: List[Node]):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        self.localSymbolTable = LocalSymbolTable()
        self.globalSymbolTable = SymbolTable()
        funcDec = self.globalSymbolTable.getter(self.value)[1]
        # Check if the number of arguments passed is greater than the number of arguments declared
        if len(self.children) > len(funcDec.children) - 2:
            raise Exception("Too many arguments passed")
        # Iterate over child 2 to n-1 to declare FuncDec variables
        # print(self.children)
        # print("Local Symbol Table")
        # print(self.localSymbolTable.table)
        for i in range(0, len(self.children)):
            # print(i)
            # Declare the funcDec variable
            # print(funcDec.children[i+1])
            funcDec.children[i+1].evaluate(self.localSymbolTable)
            # Get the identifier from the previous declaration
            iden = funcDec.children[i+1].children[0].value
            # print(iden)
            # Save the argument passed with the indeitifier
            self.localSymbolTable.setter(
                iden, self.children[i].evaluate(self.globalSymbolTable))
        # print("Local Symbol Table")
        # print(self.localSymbolTable.table)
        # Evaluate block
        result = funcDec.children[-1].evaluate(self.localSymbolTable)
        # Check if the function returns a value
        if result is not None:
            # Check if the function returns a value of the same type as the function declaration
            if funcDec.value != result[0]:
                raise Exception("Invalid return type")
            return result


class ReturnException(Exception):
    pass


class Return(Node):
    def __init__(self, value, children: List[Node]):
        self.value = value
        self.children = children

    def evaluate(self, symbolTable=None):
        if symbolTable is None:
            raise Exception("Return statement outside function")
        else:
            self.symbolTable = symbolTable
        raise ReturnException(self.children[0].evaluate(symbolTable))
