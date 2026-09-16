from sympy import diff, simplify
from math_engine.parser import create_function

class MathEngine:
    def parse(self,expression):
        return create_function(expression)

    def derivative(self, expression,order=1):
        return diff(expression,'x',order)

    def simplify(self,expression):
        return simplify(expression)

    def is_zero(self,expression):
        return simplify(expression)==0