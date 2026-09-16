import json
import os
import random

class DataLoader:
    def __init__(self, filepath="data/functions.json", error_filepath="data/math_errors.json"):
        self.filepath = filepath
        self.error_filepath = error_filepath
        self.functions = self.load_functions()
        self.error_messages = self.load_math_errors()

    def load_functions(self):
        """Carga las funciones desde el JSON de forma segura."""
        if not os.path.exists(self.filepath):
            print(f"Advertencia: No se encontró {self.filepath}")
            return []
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("functions", [])
        except Exception as e:
            print(f"Error cargando el JSON de funciones: {e}")
            return []

    def load_math_errors(self):
        """Carga las notificaciones de teoremas y easter eggs."""
        if not os.path.exists(self.error_filepath):
            return {}
        try:
            with open(self.error_filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error cargando el JSON de errores: {e}")
            return {}

    def get_all_functions(self):
        """Retorna la lista completa de funciones para la Bitácora de Funciones."""
        return self.functions

    def get_functions_for_wave(self, wave_number):
        """Filtra expresiones disponibles según el nivel de oleada actual."""
        available_expressions = [
            f["expression"] for f in self.functions 
            if f.get("oleada_minima", 1) <= wave_number
        ]
        return available_expressions if available_expressions else ["x**2"]

    def get_random_error(self, category):
        """Selecciona un mensaje de error según los pesos asignados."""
        category_list = self.error_messages.get(category, [])
        if not category_list:
            return "¡Error matemático detectado!"
        
        messages = [item["msg"] for item in category_list]
        weights = [item["weight"] for item in category_list]
        
        return random.choices(messages, weights=weights, k=1)[0]