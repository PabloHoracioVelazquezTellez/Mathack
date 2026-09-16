import random
import math
from core.enemy import FunctionEnemy
from data.data_loader import DataLoader

class WaveManager:
    def __init__(self, coordinate_system):
        self.plane = coordinate_system
        self.data_loader = DataLoader() # Carga el JSON dinámicamente
        self.current_wave = 1
        self.enemies_in_wave = []
        self.spawn_timer = 0
        self.spawn_delay = 180  # Frames entre spawns (~3 segundos a 60 FPS)
        self.wave_active = False

    def start_next_wave(self):
        """Prepara los enemigos de la oleada consultando el JSON"""
        # Obtiene expresiones disponibles para el nivel de oleada actual
        pool = self.data_loader.get_functions_for_wave(self.current_wave)
        
        # Cantidad de enemigos por oleada
        enemy_count = 3 + self.current_wave * 2
        
        self.enemies_in_wave = [random.choice(pool) for _ in range(enemy_count)]
        self.wave_active = True
        self.spawn_timer = 0

    def update(self, active_enemies_list):
        if not self.wave_active:
            return

        self.spawn_timer += 1
        
        if self.spawn_timer >= self.spawn_delay and self.enemies_in_wave:
            expr = self.enemies_in_wave.pop(0)
            new_enemy = self._create_enemy_at_border(expr)
            active_enemies_list.append(new_enemy)
            self.spawn_timer = 0

        if not self.enemies_in_wave and len(active_enemies_list) == 0:
            self.wave_active = False
            self.current_wave += 1

    def _create_enemy_at_border(self, expression_str):
        angle = random.uniform(0, 2 * math.pi)
        distance = 12.0
        
        pos_x = distance * math.cos(angle)
        pos_y = distance * math.sin(angle)
        
        speed = 0.008 + (self.current_wave * 0.002)
        
        return FunctionEnemy(expression_str, pos_x=pos_x, pos_y=pos_y, speed=speed)