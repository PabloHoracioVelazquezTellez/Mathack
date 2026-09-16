from sympy import symbols
from sympy.parsing.sympy_parser import parse_expr

x=symbols('x')
def create_function(expression):
    return parse_expr(expression)
