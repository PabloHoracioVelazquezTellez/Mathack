import pygame
from graphics.renderer import Renderer
from graphics.ui_menu import UIMenuManager
from math_engine.coordinate_system import CoordinateSystem
from core.wave_manager import WaveManager
from core.operators import (
    DerivativeOperator, 
    MultiplyByXOperator, 
    SubtractConstantOperator,
    EvaluateAtZeroOperator,
    IdentitySubtractOperator
)

def main():
    width, height = 1280, 720
    renderer = Renderer(width=width, height=height)
    plane = CoordinateSystem(width=width, height=height, scale=45)
    ui_menu = UIMenuManager(width=width, height=height)
    
    # Estados del juego
    STATE_MENU = 0
    STATE_GAME = 1
    STATE_INSTRUCTIONS = 2
    STATE_ENCYCLOPEDIA = 3
    current_state = STATE_MENU

    wave_manager = None
    enemies = []
    player_lives = 3
    selected_enemy_index = 0

    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # ---------------- GESTIÓN DE EVENTOS EN MENÚ PRINCIPAL ----------------
            if current_state == STATE_MENU:
                if ui_menu.show_objective_popup:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        ui_menu.show_objective_popup = False
                else:
                    if ui_menu.btn_play.is_clicked(mouse_pos, event.type):
                        current_state = STATE_GAME
                        wave_manager = WaveManager(plane)
                        enemies = []
                        player_lives = 3
                        selected_enemy_index = 0
                        renderer.floating_texts.clear()
                        wave_manager.start_next_wave()

                    elif ui_menu.btn_instructions.is_clicked(mouse_pos, event.type):
                        current_state = STATE_INSTRUCTIONS

                    elif ui_menu.btn_objective.is_clicked(mouse_pos, event.type):
                        ui_menu.show_objective_popup = True

                    elif ui_menu.btn_encyclopedia.is_clicked(mouse_pos, event.type):
                        current_state = STATE_ENCYCLOPEDIA

            # ---------------- GESTIÓN DE EVENTOS EN NAVEGACIÓN ----------------
            elif current_state in (STATE_INSTRUCTIONS, STATE_ENCYCLOPEDIA):
                if ui_menu.btn_back.is_clicked(mouse_pos, event.type):
                    current_state = STATE_MENU
                elif current_state == STATE_ENCYCLOPEDIA and event.type == pygame.MOUSEBUTTONDOWN:
                    ui_menu.handle_encyclopedia_click(mouse_pos)

            # ---------------- GESTIÓN DE EVENTOS DENTRO DEL JUEGO ----------------
            elif current_state == STATE_GAME:
                # Selección de objetivo por clic
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = mouse_pos
                    math_x, math_y = plane.from_screen(mx, my)
                    for idx, enemy in enumerate(enemies):
                        if enemy.is_clicked(math_x, math_y):
                            selected_enemy_index = idx
                            break

                # Selección y aplicación de operadores por teclado
                elif event.type == pygame.KEYDOWN and enemies:
                    selected_enemy_index = min(selected_enemy_index, len(enemies) - 1)
                    target = enemies[selected_enemy_index]
                    
                    operator = None
                    if event.key == pygame.K_d:
                        operator = DerivativeOperator(order=1)
                    elif event.key == pygame.K_x:
                        operator = MultiplyByXOperator()
                    elif event.key == pygame.K_c:
                        operator = SubtractConstantOperator(1)
                    elif event.key == pygame.K_e:
                        operator = EvaluateAtZeroOperator()
                    elif event.key == pygame.K_r:
                        operator = IdentitySubtractOperator()

                    if operator:
                        success, error_msg = target.apply_operator(operator, data_loader=ui_menu.data_loader)
                        
                        # Si viola un teorema o falla, se genera el texto flotante animado sobre el enemigo
                        if not success and error_msg:
                            sx, sy = plane.to_screen(target.pos_x, target.pos_y)
                            renderer.add_floating_error(error_msg, sx, sy - 40)

        # ---------------- RENDERIZADO Y LÓGICA SEGÚN EL ESTADO ----------------
        if current_state == STATE_MENU:
            ui_menu.draw_main_menu(renderer.screen, mouse_pos)
            
        elif current_state == STATE_INSTRUCTIONS:
            ui_menu.draw_instructions(renderer.screen, mouse_pos)
            
        elif current_state == STATE_ENCYCLOPEDIA:
            ui_menu.draw_encyclopedia(renderer.screen, mouse_pos)
            
        elif current_state == STATE_GAME:
            # 1. Actualización de oleadas y enemigos
            wave_manager.update(enemies)
            if not wave_manager.wave_active and len(enemies) == 0:
                wave_manager.start_next_wave()

            for enemy in enemies:
                if enemy.move_towards_origin():
                    player_lives -= 1

            # Filtrar enemigos destruidos o que colisionaron
            enemies = [e for e in enemies if e.alive]
            if enemies and selected_enemy_index >= len(enemies):
                selected_enemy_index = len(enemies) - 1

            selected_target = enemies[selected_enemy_index] if enemies else None

            # Condición de Game Over
            if player_lives <= 0:
                current_state = STATE_MENU  # Retorna al menú principal al perder

            # 2. Renderizado del tablero y entidades
            renderer.clear()
            renderer.draw_axes(plane)
            renderer.draw_player(plane)

            for idx, enemy in enumerate(enemies):
                is_sel = (idx == selected_enemy_index)
                color = (255, 220, 80) if is_sel else (70, 80, 100)
                segments = enemy.get_segments(render_range=3.5)
                renderer.draw_function(segments, plane, color=color, is_selected=is_sel)
                renderer.draw_enemy_ui(enemy, plane, is_selected=is_sel)

            # 3. Renderizado del HUD y textos flotantes de error/easter egg
            renderer.draw_hud(selected_target)
            renderer.update_and_draw_floating_texts()

        renderer.update()
        renderer.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()