import pygame
import sys
import os

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
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 74)
        self.font_button = pygame.font.Font(None, 50)
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_BLUE = (173, 216, 230)
        self.DARK_BLUE = (0, 0, 139)
        
        # Button definitions
        self.buttons = {
            "creator": pygame.Rect(width/2 - 200, height/2 - 100, 400, 80),
            "tester": pygame.Rect(width/2 - 200, height/2 + 0, 400, 80),
            "quit": pygame.Rect(width/2 - 200, height/2 + 100, 400, 80)
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
        self.screen.fill(self.BLACK)
        
        # Title
        self.draw_text("Spritesheet Tools", self.font_title, self.WHITE, self.screen, self.width/2, self.height/4)
        
        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        
        # Creator Button
        pygame.draw.rect(self.screen, self.LIGHT_BLUE, self.buttons["creator"])
        self.draw_text("Create Spritesheet", self.font_button, self.DARK_BLUE, self.screen, self.buttons["creator"].centerx, self.buttons["creator"].centery)

        # Tester Button
        pygame.draw.rect(self.screen, self.LIGHT_BLUE, self.buttons["tester"])
        self.draw_text("Test Spritesheet", self.font_button, self.DARK_BLUE, self.screen, self.buttons["tester"].centerx, self.buttons["tester"].centery)

        # Quit Button
        pygame.draw.rect(self.screen, self.LIGHT_BLUE, self.buttons["quit"])
        self.draw_text("Quit", self.font_button, self.DARK_BLUE, self.screen, self.buttons["quit"].centerx, self.buttons["quit"].centery)
        
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