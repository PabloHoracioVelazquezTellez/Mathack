import sympy as sp
import numpy as np

def compile_expression(expression):
    """Convierte la expresión de SymPy en una función ejecutable de NumPy."""
    x = sp.Symbol('x')
    return sp.lambdify(x, expression, modules=['numpy', 'math'])

def generate_segments(expression, start, end, step=0.05):
    x_symbol = sp.Symbol('x')
    
    # Manejo de expresiones constantes (ej: y = 3)
    if not expression.has(x_symbol):
        try:
            val = float(expression)
            return [[(start, val), (end, val)]]
        except Exception:
            return []

    func = compile_expression(expression)
    
    num_points = max(100, int((end - start) / step))
    x_vals = np.linspace(start, end, num_points)
    
    try:
        y_vals = func(x_vals)
        if not isinstance(y_vals, np.ndarray):
            y_vals = np.full_like(x_vals, float(y_vals))
    except Exception:
        return []

    segments = []
    current_segment = []
    prev_y = None

    # Límite máximo de salto vertical entre dos puntos continuos
    MAX_DELTA_Y = 15.0 

    for vx, vy in zip(x_vals, y_vals):
        # 1. Filtro de valores no válidos (NaN, Infinito, Complejos)
        if np.isnan(vy) or np.isinf(vy) or isinstance(vy, complex):
            if current_segment:
                segments.append(current_segment)
                current_segment = []
            prev_y = None
            continue

        vy_float = float(vy)

        # 2. Detección de discontinuidades/asíntotas por salto brusco
        if prev_y is not None:
            if abs(vy_float - prev_y) > MAX_DELTA_Y:
                if current_segment:
                    segments.append(current_segment)
                    current_segment = []

        current_segment.append((float(vx), vy_float))
        prev_y = vy_float

    if current_segment:
        segments.append(current_segment)

    return segments