import sympy as sp
from math_engine.engine import MathEngine

class DerivativeOperator:
    """Aplica derivada de orden n"""
    def __init__(self, order=1):
        self.order = order
        self.engine = MathEngine()

    def apply(self, expression):
        return self.engine.derivative(expression, self.order)

class MultiplyByXOperator:
    """Multiplica la expresión por x"""
    def apply(self, expression):
        x = sp.Symbol('x')
        return expression * x

class SubtractConstantOperator:
    """Resta un valor constante k a la expresión"""
    def __init__(self, value=1):
        self.value = value

    def apply(self, expression):
        return expression - self.value

class AddConstantOperator:
    """Suma un valor constante k a la expresión"""
    def __init__(self, value=1):
        self.value = value

    def apply(self, expression):
        return expression + self.value

class IntegralOperator:
    """Integra la expresión respecto a x (sin constante C)"""
    def apply(self, expression):
        x = sp.Symbol('x')
        return sp.integrate(expression, x)


class EvaluateAtZeroOperator:
    """Evaluar funciones en x=0"""
    def apply(self,expression):
        x=sp.Symbol('x')
        return expression.subs(x,0)

class IdentitySubtractOperator:
    #Restar la misma funcion a si misma f(x)-f(x=)=0
    def apply(self, expression):
        return expression-expression