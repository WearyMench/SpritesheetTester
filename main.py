import pygame
import sys
import os
from ui_theme import BG, SURFACE, TEXT, MUTED, ACCENT, BORDER, font, text, rounded_panel, button, configure_window

# Import tools
from spritesheet_creator import SpritesheetCreator
from spritesheet_tester import SpritesheetTester

class MainMenu:
    def __init__(self, width=1200, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Spritesheet Tools")
        configure_window()
        self.clock = pygame.time.Clock()
        self.font_title = font(48, True)
        self.font_subtitle = font(19)
        self.font_button = font(22, True)
        self.font_small = font(14)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_BLUE = (173, 216, 230)
        self.DARK_BLUE = (0, 0, 139)
        
        # Button definitions
        self.buttons = {
            "creator": pygame.Rect(width/2 - 230, height/2 - 40, 460, 70),
            "tester": pygame.Rect(width/2 - 230, height/2 + 48, 460, 70),
            "quit": pygame.Rect(width/2 - 230, height/2 + 148, 460, 50)
        }
        
    def draw_text(self, text, font, color, surface, x, y, center=True):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        if center:
            textrect.center = (x, y)
        else:
            textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def draw_menu(self):
        self.screen.fill(BG)
        text(self.screen, "SPRITESHEET STUDIO", self.font_small, ACCENT, (self.width/2, 118), center=True)
        text(self.screen, "Da vida a tus sprites", self.font_title, TEXT, (self.width/2, 170), center=True)
        text(self.screen, "Crea, ajusta y previsualiza animaciones en un solo lugar.", self.font_subtitle, MUTED, (self.width/2, 214), center=True)
        card = pygame.Rect(self.width/2 - 260, 272, 520, 360)
        rounded_panel(self.screen, card, SURFACE, BORDER, 20)
        mouse_pos = pygame.mouse.get_pos()
        text(self.screen, "¿Qué quieres hacer?", font(18, True), TEXT, (self.width/2 - 230, 298))
        button(self.screen, self.buttons["creator"], "Crear spritesheet", self.font_button, mouse_pos, primary=True)
        button(self.screen, self.buttons["tester"], "Probar una animación", self.font_button, mouse_pos)
        button(self.screen, self.buttons["quit"], "Salir", font(17), mouse_pos)
        text(self.screen, "También puedes usar el teclado dentro de cada herramienta", self.font_small, MUTED, (self.width/2, 676), center=True)
        
        pygame.display.flip()

    def run(self):
        while True:
            self.draw_menu()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if self.buttons["creator"].collidepoint(mouse_pos):
                            return "creator"
                        if self.buttons["tester"].collidepoint(mouse_pos):
                            return "tester"
                        if self.buttons["quit"].collidepoint(mouse_pos):
                            pygame.quit()
                            sys.exit()
            
            self.clock.tick(60)

if __name__ == "__main__":
    app_state = "main_menu"
    current_spritesheet_path = None # To pass path from creator to tester

    main_screen = pygame.display.set_mode((1200, 800))

    while True:
        if app_state == "main_menu":
            menu = MainMenu()
            app_state = menu.run()
        
        elif app_state == "creator":
            creator = SpritesheetCreator()
            result = creator.run()
            
            if result.get("action") == "test":
                app_state = "tester"
                current_spritesheet_path = result.get("path")
            else:
                app_state = "main_menu"

        elif app_state == "tester":
            tester = SpritesheetTester()
            tester.run(spritesheet_path=current_spritesheet_path)
            current_spritesheet_path = None # Clear path after use
            app_state = "main_menu"
        
        else: # Quit
            pygame.quit()
            sys.exit()
