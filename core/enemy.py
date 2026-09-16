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

    def apply_operator(self, operator):
        """Aplica el operador y evalúa si causó daño real o si eliminó la función"""
        new_expr = operator.apply(self.expression)
        new_expr = self.engine.simplify(new_expr)
        
        # 1. Verificar si la función fue destruida por completo (llegó a 0)
        if self.engine.is_zero(new_expr):
            self.expression = new_expr
            self.raw_expression_str = "0"
            self.alive = False
            self.health = 0
            return

        # 2. Calcular complejidades previa y nueva
        old_complexity = self._calculate_complexity(self.expression)
        new_complexity = self._calculate_complexity(new_expr)

        # Actualizar la expresión
        self.expression = new_expr
        self.raw_expression_str = str(self.expression)

        # 3. Lógica de Daño/Salud:
        if new_complexity < old_complexity:
            # Hubo daño efectivo (ej: derivada redujo el grado)
            self.health -= (old_complexity - new_complexity)
        else:
            # Se transformó o multiplicó por x: se recalcula la salud máxima acorde a la nueva función
            self.max_health = max(self.max_health, new_complexity)
            self.health = new_complexity

        # Verificar muerte por salud agotada
        if self.health <= 0:
            self.alive = False

    def get_segments(self, render_range=4, step=0.02):
        x = sp.Symbol('x')
        shifted_expr = self.expression.subs(x, x - self.pos_x) + self.pos_y
        return generate_segments(
            shifted_expr, 
            start=self.pos_x - render_range, 
            end=self.pos_x + render_range, 
            step=step
        )