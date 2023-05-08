from rply.token import BaseBox
from abc import abstractmethod


class Node(BaseBox):
    def __init__(self, value):
        self.value = value

    # @abstractmethod
    # def eval(self):
    #     pass


class Program(Node):
    def __init__(self, statements):
        self.statements = statements

    def eval(self):
        #     for statement in self.statements:
        #         statement.eval()


class Int():
    def __init__(self, value):
        self.value = value

    def eval(self):
        #     return int(self.value)


class BinaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class UnaryOp():
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Sum(BinaryOp):
    # def eval(self):
    # return self.left.eval() + self.right.eval()


class Sub(BinaryOp):
    # def eval(self):
    # return self.left.eval() - self.right.eval()


class Mul(BinaryOp):
    # def eval(self):
    # return self.left.eval() * self.right.eval()


class Div(BinaryOp):
    # def eval(self):
    # return self.left.eval() // self.right.eval()


class Print():
    def __init__(self, value):
        self.value = value

    # def eval(self):
        # print(self.value.eval())
