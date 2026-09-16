import json
import os

class DataLoader:
    def __init__(self, filepath="data/functions.json"):
        self.filepath=filepath
        self.functions=self.load_functions()

    def load_functions(self):
        """para argar el JSON"""
        if not os.path.exists(self.filepath):
            print(f"NO SE ENCONTRO {self.filepath}")
            return []

        try:
            with open(self.filepath,'r', encoding='utf-8') as f:
                data=json.load(f)
                return data.get("functions",[])
        except Exception as e:
            print(f"ERROR AL CARGAR EL JSON:{e}")
            return []

    def get_all_functions(self):
        """"PARA RETORNAR LA LISTA COMPLETA PARA LA BITACORA"""
        return self.functions

    def get_functions_for_wave(self,wave_number):
        """para filtrar las expresiones disponibles segun la oleada"""
        available_expressions=[f["expression"] fot f in self.functions if f.get("oleada_minima",1)<=wave_number]
        return available_expressions if available_expressions else ["x**2"]
    