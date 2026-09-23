import pygame
from graphics.particles import ParticleSystem

class Renderer:
    def __init__(self, width=1280, height=720):
        pygame.init()
        pygame.font.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        self.particle_system=ParticleSystem()
        pygame.display.set_caption("Mathack - Math Combat Engine")
        self.clock = pygame.time.Clock()
        
        # Fuentes para UI
        self.font_enemy = pygame.font.SysFont("Consolas", 18, bold=True)
        self.font_hud = pygame.font.SysFont("Consolas", 16, bold=True)
        self.font_title = pygame.font.SysFont("Consolas", 22, bold=True)
        self.floating_texts = []
        self.font_error = pygame.font.SysFont("Consolas", 15, bold=True)

    def add_floating_error(self, text, screen_x, screen_y):
        self.floating_texts.append(FloatingText(text, screen_x, screen_y))

    def update_and_draw_floating_texts(self):
        for ft in self.floating_texts[:]:
            ft.update()
            if ft.lifetime <= 0:
                self.floating_texts.remove(ft)
            else:
                # Renderizado con fondo oscuro
                surf = self.font_error.render(ft.text, True, ft.color)
                rect = surf.get_rect(center=(int(ft.x), int(ft.y)))
                bg_rect = rect.inflate(10, 6)
                pygame.draw.rect(self.screen, (15, 15, 25), bg_rect, border_radius=4)
                pygame.draw.rect(self.screen, (255, 85, 85), bg_rect, width=1, border_radius=4)
                self.screen.blit(surf, rect)
                
    def clear(self):
        self.screen.fill((15, 15, 22)) # Fondo oscuro espacial

    def update(self):
        pygame.display.flip()

    def tick(self, fps=60):
        self.clock.tick(fps)

    def draw_axes(self, coordinate_system):
        # Grilla secundaria tenue
        grid_color = (30, 35, 45)
        axis_color = (80, 90, 110)
        
        # Ejes principales
        pygame.draw.line(self.screen, axis_color, (0, coordinate_system.origin_y), (self.width, coordinate_system.origin_y), 2)
        pygame.draw.line(self.screen, axis_color, (coordinate_system.origin_x, 0), (coordinate_system.origin_x, self.height), 2)

    def draw_player(self, coordinate_system):
        x, y = coordinate_system.to_screen(0, 0)
        # Núcleo del jugador con aura
        pygame.draw.circle(self.screen, (0, 255, 180, 50), (int(x), int(y)), 14)
        pygame.draw.circle(self.screen, (0, 255, 150), (int(x), int(y)), 8)

    def draw_function(self, segments, coordinate_system, color=(255, 255, 255), is_selected=False):
        # Si está seleccionado, la línea es más gruesa; si no, es un láser delgado y discreto
        width = 3 if is_selected else 1
        
        for segment in segments:
            if len(segment) < 2:
                continue
            screen_points = []
            for x, y in segment:
                sx, sy = coordinate_system.to_screen(x, y)
                try:
                    px, py = int(float(sx)), int(float(sy))
                    if -500 <= px <= self.width + 500 and -500 <= py <= self.height + 500:
                        screen_points.append((px, py))
                except (ValueError, TypeError, OverflowError):
                    continue
            
            if len(screen_points) >= 2:
                pygame.draw.lines(self.screen, color, False, screen_points, width)

    def draw_enemy_ui(self, enemy, coordinate_system, is_selected=False):
        """Renderiza el texto de la función y la barra de complejidad flotante."""
        sx, sy = coordinate_system.to_screen(enemy.pos_x, enemy.pos_y)
        px, py = int(sx), int(sy)

        # 1. Etiqueta con la expresión matemática actual
        expr_text = f"f(x) = {enemy.raw_expression_str}"
        text_color = (255, 255, 255) if is_selected else (180, 180, 190)
        surface_text = self.font_enemy.render(expr_text, True, text_color)
        
        # Fondo oscuro para la etiqueta
        text_rect = surface_text.get_rect(center=(px, py - 35))
        bg_rect = text_rect.inflate(12, 6)
        pygame.draw.rect(self.screen, (20, 20, 30), bg_rect, border_radius=4)
        if is_selected:
            pygame.draw.rect(self.screen, (255, 200, 0), bg_rect, width=2, border_radius=4)
        self.screen.blit(surface_text, text_rect)

        # 2. Barra de Complejidad (Salud del Enemigo)
        bar_w, bar_h = 60, 6
        bar_x = px - bar_w // 2
        bar_y = py - 18

        pct = max(0.0, min(1.0, enemy.health / float(enemy.max_health)))
        fill_w = int(bar_w * pct)

        # Color según el nivel de complejidad restante
        color_bar = (0, 220, 255) if pct > 0.5 else ((255, 200, 0) if pct > 0.25 else (255, 50, 80))

        pygame.draw.rect(self.screen, (40, 40, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=3)
        if fill_w > 0:
            pygame.draw.rect(self.screen, color_bar, (bar_x, bar_y, fill_w, bar_h), border_radius=3)

    def draw_hud(self, selected_enemy=None):
        """Dibuja la barra inferior con los operadores disponibles."""
        hud_h = 60
        hud_rect = pygame.Rect(0, self.height - hud_h, self.width, hud_h)
        pygame.draw.rect(self.screen, (10, 12, 18), hud_rect)
        pygame.draw.line(self.screen, (50, 60, 80), (0, self.height - hud_h), (self.width, self.height - hud_h), 2)

        # Lista de comandos disponibles en el teclado
        commands = [
            ("[D]", "Derivar d/dx"),
            ("[X]", "Multiplicar (*x)"),
            ("[C]", "Restar constante (-1)"),
            ("[E]","Evaluar x=0"),
            ("[R]","Anular f(x)")
        ]

        # Dibujar botones de comandos
        start_x = 30
        for key, desc in commands:
            cmd_text = f"{key} {desc}"
            txt_surf = self.font_hud.render(cmd_text, True, (0, 220, 255))
            self.screen.blit(txt_surf, (start_x, self.height - 38))
            start_x += 240

        # Estado del objetivo actual
        if selected_enemy:
            target_info = f"OBJETIVO: f(x) = {selected_enemy.raw_expression_str} | COMPLEJIDAD: {selected_enemy.health}/{selected_enemy.max_health}"
            info_surf = self.font_hud.render(target_info, True, (255, 200, 0))
            self.screen.blit(info_surf, (self.width - info_surf.get_width() - 30, self.height - 38))


    def add_explosion(self, screen_x, screen_y, count=35):
        """Gatilla una explosión visual en coordenadas de pantalla"""
        self.particle_system.emit_explosion(screen_x, screen_y, count=count)

    def update_and_draw_particles(self):
        self.particle_system.update_and_draw(self.screen)

class FloatingText:
    def __init__(self, text, x, y, color=(255, 85, 85)):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = 110  # ~1.8 segundos a 60 FPS
        
    def update(self):
        self.y -= 0.6  # Sube lentamente
        self.lifetime -= 1

