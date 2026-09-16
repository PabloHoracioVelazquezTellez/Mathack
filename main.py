import pygame
from graphics.renderer import Renderer
from math_engine.coordinate_system import CoordinateSystem
from core.wave_manager import WaveManager
from core.operators import (DerivativeOperator, MultiplyByXOperator, SubtractConstantOperator,EvaluateAtZeroOperator,IdentitySubstractOperator)

def main():
    width, height = 1280, 720
    renderer = Renderer(width=width, height=height)
    plane = CoordinateSystem(width=width, height=height, scale=40)
    
    wave_manager = WaveManager(spawn_radius=14.0)
    enemies = []
    
    selected_enemy_index = 0
    player_hp = 3
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Selección por clic
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                math_x, math_y = plane.from_screen(mx, my)
                
                for idx, enemy in enumerate(enemies):
                    if enemy.is_clicked(math_x, math_y):
                        selected_enemy_index = idx
                        break

            elif event.type == pygame.KEYDOWN and enemies:
                selected_enemy_index = min(selected_enemy_index, len(enemies) - 1)
                target = enemies[selected_enemy_index]
                
                if event.key==pygame.K_d:
                    target.apply_operator(DerivativeOperator(order=1))
                elif event.key==pygame.K_x:
                    target.apply_operator(MultiplyByXOperator())
                elif event.key==pygame.K_c:
                    target.apply_operator(SubtractConstantOperator(1))
                elif event.key==pygame.K_e:
                    target.apply_operator(EvaluateAtZeroOperator())
                elif event.key==pygame.K_r:
                    target.apply_operator(IdentitySubstractOperator())

        # Actualizar Spawner de Oleadas
        new_enemy = wave_manager.update(enemies)
        if new_enemy:
            enemies.append(new_enemy)

        # Actualizar Movimiento de Enemigos
        for enemy in enemies[:]:
            reached_origin = enemy.move_towards_origin()
            if reached_origin:
                player_hp -= 1  # Daño al jugador si toca el origen
                print(f"¡Impacto recibido! HP restante: {player_hp}")

        # Filtrar enemigos destruidos o que llegaron al centro
        surviving_enemies = []
        for enemy in enemies:
            if enemy.alive:
                surviving_enemies.append(enemy)
            else:
                score += 100  # Puntuación por eliminación
        
        enemies = surviving_enemies

        if enemies and selected_enemy_index >= len(enemies):
            selected_enemy_index = max(0, len(enemies) - 1)

        selected_target = enemies[selected_enemy_index] if enemies else None

        # RENDERIZADO
        renderer.clear()
        renderer.draw_axes(plane)
        renderer.draw_player(plane)

        for idx, enemy in enumerate(enemies):
            is_sel = (idx == selected_enemy_index)
            color = (255, 220, 80) if is_sel else (70, 80, 100)
            
            segments = enemy.get_segments(render_range=3.0)
            renderer.draw_function(segments, plane, color=color, is_selected=is_sel)
            renderer.draw_enemy_ui(enemy, plane, is_selected=is_sel)

        renderer.draw_hud(selected_target)

        # Condición simple de Fin de Juego
        if player_hp <= 0:
            print(f"GAME OVER. Puntuación final: {score}")
            running = False

        renderer.update()
        renderer.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()