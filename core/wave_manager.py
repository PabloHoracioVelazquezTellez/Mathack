import random
import math 
from core.enemy import FunctionEnemy

class WaveManager:
    def __init__(self,spawn_radius=12.0):
        self.spawn_radius=spawn_radius
        self.current_wave=1
        self.enemies_spawned_in_wave=0
        self.enemies_per_wave=4
        self.spawn_timer=0
        self.spawn_cooldown=180
        self.wave_in_progress=True

        self.pool_wave_1=["2","3","x","x+1"]
        self.pool_wave_2=["x**2","x**2 -1","2*x +3","1/x"]
        self.pool_wave_3=["x**3","1/(x**2)","sin(x)","exp(x)"]


    def _get_random_spawn_pos(self):
        angle=random.uniform(0,2*math.pi)
        x=self.spawn_radius*math.cos(angle)
        y=self.spawn_radius*math.sin(angle)
        return x,y

    def _select_expression(self):
        if self.current_wave==1:
            return random.choice(self.pool_wave_1)
        elif self.current_wave==2:
            return random.choice(self.pool_wave_2)
        else:
            pool=self.pool_wave_2+self.pool_wave_3
            return random.choice(pool)

    def update(self,active_enemies):
        self.spawn_timer +=1
        if self.enemies_spawned_in_wave<self.enemies_per_wave:
            if self.spawn_timer>=self.spawn_cooldown:
                self.spawn_timer=0
                expr=self._select_expression()
                x,y=self._get_random_spawn_pos()
                speed=0.008 +(self.current_wave*0.002)
                self.enemies_spawned_in_wave+=1
                return FunctionEnemy(expr,pos_x=x,pos_y=y,speed=speed)
        elif len(active_enemies)==0:
            self.current_wave +=1
            self.enemies_spawned_in_wave=0
            self.enemies_per_wave +=2
            self.spawn_cooldown=max(60,self.spawn_cooldown -15)
            self.spawn_timer=0
        return None