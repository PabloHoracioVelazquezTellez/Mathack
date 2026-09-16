import math
import sympy as sp
from math_engine.engine import MathEngine
from math_engine.evaluator import generate_segments

class FunctionEnemy:
    def __init__(self, expression_str, pos_x=0.0, pos_y=0.0, speed=0.005):
        self.engine = MathEngine()
        self.raw_expression_str = expression_str
        self.expression = self.engine.parse(expression_str)
        
        # Posición
        self.pos_x = float(pos_x)
        self.pos_y = float(pos_y)
        self.speed = speed
        self.alive = True
        
        self.max_health = self._calculate_complexity(self.expression)
        self.health = self.max_health


    def move_towards_origin(self):
        angle = math.atan2(-self.pos_y, -self.pos_x)
        self.pos_x += self.speed * math.cos(angle)
        self.pos_y += self.speed * math.sin(angle)
        
        if math.hypot(self.pos_x, self.pos_y) < 0.2:
            self.alive = False
            return True
        return False

    def is_clicked(self, math_x, math_y, threshold=1.5):
        return math.hypot(math_x - self.pos_x, math_y - self.pos_y) <= threshold
    
    def _calculate_complexity(self, expr):
        """Calcula el nivel de complejidad actual de la expresión"""
        x = sp.Symbol('x')
        try:
            poly = sp.Poly(expr, x)
            return max(1, poly.degree() + 1)
        except Exception:
            return 3  # Valor base para racionales/trascendentes

    def apply_operator(self, operator, data_loader=None):
        """
        Aplica un operador matemático al enemigo validando teoremas.
        Retorna (exito: bool, mensaje_error: str or None)
        """
        expr_str = str(self.expression)
        op_name = operator.__class__.__name__

        # -------------------------------------------------------------------
        # 1. VALIDACIÓN DE TEOREMAS Y REGLAS (DESPLIEGUE DE AVISOS Y EASTER EGGS)
        # -------------------------------------------------------------------
        if data_loader:
            # A) Intentar derivar funciones no derivables o con puntos angulosos (|x|)
            if op_name == "DerivativeOperator" and "Abs" in expr_str:
                return False, data_loader.get_random_error("NON_DIFFERENTIABLE")

            # B) Intentar evaluar x=0 en discontinuidades esenciales / división por cero (1/x)
            if op_name == "EvaluateAtZeroOperator" and ("/x" in expr_str or "1/x" in expr_str):
                return False, data_loader.get_random_error("DIVISION_BY_ZERO")

            # C) Intentar derivar una constante numérica con d/dx (debe usarse [C] o [E])
            if op_name == "DerivativeOperator" and self.expression.is_number:
                return False, data_loader.get_random_error("ZERO_DERIVATIVE")

            # D) Advertencia al entrar en bucles trigonométricos infinitos derivando sin/cos
            if op_name == "DerivativeOperator" and any(trig in expr_str for trig in ["sin", "cos", "tan"]):
                if random.random() < 0.30:  # 30% de probabilidad de aviso didáctico al derivar
                    return False, data_loader.get_random_error("CYCLIC_TRIGONOMETRIC")

        # -------------------------------------------------------------------
        # 2. APLICACIÓN Y SIMPLIFICACIÓN MATEMÁTICA
        # -------------------------------------------------------------------
        new_expr = operator.apply(self.expression)
        new_expr = self.engine.simplify(new_expr)

        # Caso A: Destrucción instantánea por anulación (llegó a 0)
        if self.engine.is_zero(new_expr):
            self.expression = new_expr
            self.raw_expression_str = "0"
            self.alive = False
            self.health = 0
            return True, None

        # -------------------------------------------------------------------
        # 3. CÁLCULO DE COMPLEJIDAD Y DAÑO EFECTIVO
        # -------------------------------------------------------------------
        old_complexity = self._calculate_complexity(self.expression)
        new_complexity = self._calculate_complexity(new_expr)

        # Actualizamos la expresión interna y la cadena de texto legible
        self.expression = new_expr
        self.raw_expression_str = str(self.expression)

        # Si la complejidad bajó (ej: derivada redujo el grado), sufre daño
        if new_complexity < old_complexity:
            self.health -= (old_complexity - new_complexity)
        else:
            # Si la función se transformó o multiplicó por x (ej: 1/x * x -> 1),
            # se reajusta la salud acorde al nuevo estado sin matar al enemigo sin sentido
            self.max_health = max(self.max_health, new_complexity)
            self.health = new_complexity

        # Verificar si la salud se agotó
        if self.health <= 0:
            self.alive = False
            self.health = 0

        return True, None

    def get_segments(self, render_range=4, step=0.02):
        x = sp.Symbol('x')
        shifted_expr = self.expression.subs(x, x - self.pos_x) + self.pos_y
        return generate_segments(
            shifted_expr, 
            start=self.pos_x - render_range, 
            end=self.pos_x + render_range, 
            step=step
        )