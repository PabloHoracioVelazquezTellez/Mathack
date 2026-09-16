import pygame
from data.data_loader import DataLoader
class Button:
    def __init__(self, x, y, width, height, text, font, bg_color=(30, 35, 50), hover_color=(50, 60, 90), text_color=(0, 220, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (0, 200, 255) if self.is_hovered else (80, 90, 110), self.rect, width=2, border_radius=8)
        
        txt_surf = self.font.render(self.text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered

    def is_clicked(self, mouse_pos, event_type):
        return event_type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mouse_pos)


class UIMenuManager:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
        # Fuentes
        self.font_title = pygame.font.SysFont("Consolas", 48, bold=True)
        self.font_subtitle = pygame.font.SysFont("Consolas", 18, italic=True)
        self.font_btn = pygame.font.SysFont("Consolas", 20, bold=True)
        self.font_text = pygame.font.SysFont("Consolas", 16)
        
        # Botones del Menú Principal
        cx = width // 2 - 175
        self.btn_play = Button(cx, 260, 350, 50, "EMPEZAR JUEGO", self.font_btn)
        self.btn_instructions = Button(cx, 330, 350, 50, "INSTRUCCIONES", self.font_btn)
        self.btn_objective = Button(cx, 400, 350, 50, "OBJETIVO DEL JUEGO", self.font_btn)
        self.btn_encyclopedia = Button(cx, 470, 350, 50, "BITACORA DE FUNCIONES", self.font_btn)
        
        # Botones de navegación interna
        self.btn_back = Button(40, height - 70, 160, 40, "< VOLVER", self.font_btn)
        
        # Estado de modales y enciclopedia
        self.show_objective_popup = False
        self.selected_function_index = 0

        # Datos para la Bitácora de Funciones
        self.data_loader = DataLoader()
        # Carga la base de datos completa desde el JSON
        self.function_database = self.data_loader.get_all_functions()

    def draw_main_menu(self, surface, mouse_pos):
        surface.fill((12, 14, 22))
        
        # Título Principal
        title = self.font_title.render("M A T H A C K", True, (0, 220, 255))
        subtitle = self.font_subtitle.render("Sistema de Combates Matemáticos Cartesianos", True, (140, 150, 180))
        surface.blit(title, title.get_rect(center=(self.width // 2, 120)))
        surface.blit(subtitle, subtitle.get_rect(center=(self.width // 2, 175)))
        
        # Actualizar hover y dibujar botones
        for btn in [self.btn_play, self.btn_instructions, self.btn_objective, self.btn_encyclopedia]:
            btn.check_hover(mouse_pos)
            btn.draw(surface)

        # Popup del Objetivo si está activo
        if self.show_objective_popup:
            self._draw_objective_modal(surface)

    def _draw_objective_modal(self, surface):
        # Overlay oscuro semitransparente
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        surface.blit(overlay, (0, 0))
        
        modal_rect = pygame.Rect(self.width // 2 - 350, self.height // 2 - 120, 700, 240)
        pygame.draw.rect(surface, (20, 25, 40), modal_rect, border_radius=12)
        pygame.draw.rect(surface, (0, 220, 255), modal_rect, width=2, border_radius=12)
        
        title_surf = self.font_btn.render("OBJETIVO DEL JUEGO", True, (255, 200, 0))
        surface.blit(title_surf, (modal_rect.x + 30, modal_rect.y + 25))
        
        # Mensaje personalizado
        phrase = '"Entiende un poquito de cálculo sin necesidad de reprobar en la escuela."'
        author = "ATTE: ρablotz1504"  # Uso explícito de la letra griega rho (ρ)
        
        p_surf = self.font_subtitle.render(phrase, True, (240, 240, 250))
        a_surf = self.font_btn.render(author, True, (0, 220, 255))
        
        surface.blit(p_surf, (modal_rect.x + 30, modal_rect.y + 80))
        surface.blit(a_surf, (modal_rect.x + 30, modal_rect.y + 130))
        
        close_txt = self.font_text.render("[ Haz clic en cualquier lugar para cerrar ]", True, (120, 130, 150))
        surface.blit(close_txt, (modal_rect.x + 30, modal_rect.y + 190))

    def draw_instructions(self, surface, mouse_pos):
        surface.fill((12, 14, 22))
        
        title = self.font_title.render("INSTRUCCIONES", True, (0, 220, 255))
        surface.blit(title, (50, 40))
        
        lines = [
            "1. El jugador permanece ubicado en el origen del plano cartesiano (0,0).",
            "2. Las funciones matemáticas avanzan desde los bordes del plano hacia ti.",
            "3. Haz CLIC IZQUIERDO sobre una función para seleccionarla como OBJETIVO.",
            "4. Usa los OPERADORES del teclado para modificar las expresiones y llevarlas a 0:",
            "   • [D] Derivar (d/dx): Reduce el grado de polinomios.",
            "   • [X] Multiplicar (*x): Ayuda a cancelar racionales como 1/x.",
            "   • [C] Restar constante (-1): Elimina términos constantes.",
            "   • [E] Evaluar en x=0: Anula funciones como sin(x).",
            "   • [R] Resta Identidad f(x)-f(x): Anulación total instantánea.",
            "5. Evita que las funciones colisionen con el origen para no perder vidas."
        ]
        
        y = 130
        for line in lines:
            txt_surf = self.font_text.render(line, True, (200, 210, 230))
            surface.blit(txt_surf, (50, y))
            y += 35

        self.btn_back.check_hover(mouse_pos)
        self.btn_back.draw(surface)

    def draw_encyclopedia(self, surface, mouse_pos):
        surface.fill((12, 14, 22))
        
        title = self.font_title.render("BITACORA DE FUNCIONES", True, (0, 220, 255))
        surface.blit(title, (50, 30))
        
        # Panel lateral izquierdo (Lista de Funciones)
        left_panel = pygame.Rect(50, 100, 300, 520)
        pygame.draw.rect(surface, (20, 24, 35), left_panel, border_radius=8)
        
        for idx, func in enumerate(self.function_database):
            fy = 110 + idx * 60
            f_rect = pygame.Rect(60, fy, 280, 50)
            is_sel = (idx == self.selected_function_index)
            
            bg = (40, 50, 75) if is_sel else (28, 32, 48)
            pygame.draw.rect(surface, bg, f_rect, border_radius=6)
            if is_sel:
                pygame.draw.rect(surface, (0, 220, 255), f_rect, width=2, border_radius=6)
                
            txt_surf = self.font_text.render(func["name"], True, (255, 255, 255) if is_sel else (170, 180, 200))
            surface.blit(txt_surf, (70, fy + 15))

        # Panel principal derecho (Propiedades Matemáticas y Debilidades)
        right_panel = pygame.Rect(370, 100, 860, 520)
        pygame.draw.rect(surface, (20, 24, 35), right_panel, border_radius=8)
        
        data = self.function_database[self.selected_function_index]
        
        header_surf = self.font_btn.render(f"ANALISIS MATEMATICO: {data['name']}", True, (255, 200, 0))
        surface.blit(header_surf, (400, 125))
        
        details = [
            ("Linealidad:", data["linealidad"]),
            ("Continuidad:", data["continuidad"]),
            ("Inyectividad:", data["inyectividad"]),
            ("Paridad (Par/Impar):", data["paridad"]),
            ("Complejidad en Juego:", data["complejidad"]),
            ("Debilidad / Comandos:", data["debilidad"])
        ]
        
        dy = 180
        for label, val in details:
            lbl_surf = self.font_text.render(label, True, (0, 220, 255))
            val_surf = self.font_text.render(val, True, (220, 225, 240))
            surface.blit(lbl_surf, (400, dy))
            surface.blit(val_surf, (620, dy))
            dy += 45

        self.btn_back.check_hover(mouse_pos)
        self.btn_back.draw(surface)

    def handle_encyclopedia_click(self, mouse_pos):
        """Permite cambiar de función en la lista lateral"""
        for idx in range(len(self.function_database)):
            fy = 110 + idx * 60
            f_rect = pygame.Rect(60, fy, 280, 50)
            if f_rect.collidepoint(mouse_pos):
                self.selected_function_index = idx
                break

    def draw_game_over(self, surface, wave_reached):
        """pantalla de GAME OVER y opcion de reinicio"""
        overlay=pygame.Surface((self.width,self.height), pygame.SRCALPHA)
        overlay.fill((10,10,18,220))
        surface.blit(overlay,(0,0))


        panel_rect=pygame.Rect(self.width//2-300,self.height//2-160,600,320)
        pygame.draw.rect(surface,(22,25,38),panel_rect,border_radius=12)
        pygame.draw.rect(surface,(255,60,80),panel_rect,width=2,border_radius=12)


        title_surf=self.font_title.render("G A M E      O V E R",True,(255,60,80))
        sub_surf=self.font_subtitle.render("Las funciones han colapsado el origen (0,0)", True,(180,190,210))
        wave_surf=self.font_btn.render(f"Sobreviviste hasta la Oleada: {wave_reached}",True,(255,200,0))


        surface.blit(title_surf,title_surf.get_rect(center=(self.width//2,panel_rect.y+60)))
        surface.blit(sub_surf,sub_surf.get_rect(center=(self.width//2,panel_rect.y+110)))
        surface.blit(wave_surf,wave_surf.get_rect(center=(self.width//2,panel_rect.y+165)))


        opt_enter=self.font_text.render("Presiona [ ENTER ] para Reiniciar la Partida",True,(0,220,255))
        opt_esc=self.font_text.render("Presiona [ ESC ] para Volver al Mu=enu Principal",True,(140,150,170))



        surface.blit(opt_enter,opt_enter.get_rect(center=(self.width//2,panel_rect.y+225)))
        surface.blit(opt_esc,opt_esc.get_rect(center=(self.width//2,panel_rect.y+265)))