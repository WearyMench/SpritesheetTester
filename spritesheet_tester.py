import pygame
import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
from ui_theme import (BG, SURFACE, TEXT, MUTED, ACCENT, SUCCESS, BORDER,
                      font, text, rounded_panel, checkerboard, button, toggle_button, stat,
                      configure_window)

class SpritesheetTester:
    def __init__(self, width=1200, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Spritesheet Tester")
        configure_window()
        self.clock = pygame.time.Clock()
        self.font = font(22, True)
        self.small_font = font(14)
        self.tiny_font = font(12)
        self.button_font = font(15, True)
        
        # Initialize tkinter for file dialog (hidden window)
        self.tk_root = tk.Tk()
        self.tk_root.withdraw()  # Hide the tkinter window
        
        # Spritesheet properties
        self.spritesheet = None
        self.spritesheet_path = None
        self.scaled_thumbnail_spritesheet = None
        self.frame_width = 0
        self.frame_height = 0
        self.columns = 4
        self.rows = 4
        self.total_frames = 16
        
        # Animation properties
        self.current_frame = 0
        self.animation_speed = 100  # milliseconds per frame
        self.last_frame_time = 0
        # Unknown sheets start paused to avoid unexpected rapid flashing.
        self.is_playing = False
        self.loop = True
        
        # UI properties
        self.thumbnail_scale_factor = 1.0
        self.animation_scale_factor = 3.0
        self.show_grid = True
        self.show_info = True
        self.buttons = {}
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        
    def browse_spritesheet(self):
        """Open file dialog to browse and load a spritesheet"""
        try:
            # Configure file dialog
            filetypes = [
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.tga"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
            
            # Open file dialog
            file_path = filedialog.askopenfilename(
                title="Select Spritesheet Image",
                filetypes=filetypes,
                initialdir=os.getcwd()
            )
            
            if file_path:
                # Convert to absolute path
                abs_path = os.path.abspath(file_path)
                if self.load_spritesheet(abs_path):
                    print(f"Successfully loaded: {abs_path}")
                    return True
                else:
                    messagebox.showerror("Error", f"Failed to load spritesheet:\n{abs_path}")
                    return False
        except Exception as e:
            messagebox.showerror("Error", f"Error browsing file:\n{str(e)}")
            return False
        
        return False
        
    def load_spritesheet(self, path):
        """Load a spritesheet from file"""
        try:
            self.spritesheet = pygame.image.load(path)
            self.spritesheet_path = path
            self.calculate_frame_dimensions()
            self.calculate_and_scale_assets()
            return True
        except pygame.error as e:
            print(f"Error loading spritesheet: {e}")
            return False
    
    def calculate_frame_dimensions(self):
        """Calculate frame dimensions based on columns and rows"""
        if self.spritesheet:
            self.frame_width = self.spritesheet.get_width() // self.columns
            self.frame_height = self.spritesheet.get_height() // self.rows
            self.total_frames = self.columns * self.rows
            self.calculate_and_scale_assets()
    
    def calculate_and_scale_assets(self):
        """Calculate scale factors and scale assets for thumbnail and animation."""
        if self.spritesheet:
            # Thumbnail scaling (to fit in UI panel)
            thumb_available_width = 360
            if self.spritesheet.get_width() > 0:
                thumb_scale = thumb_available_width / self.spritesheet.get_width()
                self.thumbnail_scale_factor = min(thumb_scale, 1.0)
            else:
                self.thumbnail_scale_factor = 1.0
            
            thumb_width = int(self.spritesheet.get_width() * self.thumbnail_scale_factor)
            thumb_height = int(self.spritesheet.get_height() * self.thumbnail_scale_factor)
            self.scaled_thumbnail_spritesheet = pygame.transform.scale(self.spritesheet, (thumb_width, thumb_height))

            # Animation scaling (to fit in main view)
            main_view_width = self.width - 400
            main_view_height = self.height - 100
            
            if self.frame_width > 0 and self.frame_height > 0:
                scale_x = main_view_width / self.frame_width
                scale_y = main_view_height / self.frame_height
                self.animation_scale_factor = min(scale_x, scale_y)
            else:
                self.animation_scale_factor = 1.0
    
    def get_frame_surface(self, frame_index, scale_factor=1.0):
        """Get a specific frame from the spritesheet, scaled."""
        if not self.spritesheet or frame_index >= self.total_frames or self.frame_width == 0 or self.frame_height == 0:
            return None
        
        col = frame_index % self.columns
        row = frame_index // self.columns
        
        src_x = col * self.frame_width
        src_y = row * self.frame_height
        src_rect = pygame.Rect(src_x, src_y, self.frame_width, self.frame_height)
        
        frame_surface = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        frame_surface.blit(self.spritesheet, (0, 0), src_rect)
        
        scaled_width = int(self.frame_width * scale_factor)
        scaled_height = int(self.frame_height * scale_factor)
        return pygame.transform.scale(frame_surface, (scaled_width, scaled_height))
    
    def draw_grid(self, offset_x=0, offset_y=0):
        """Draw grid lines on the spritesheet thumbnail."""
        if not self.scaled_thumbnail_spritesheet:
            return
        
        # Draw vertical lines
        for i in range(1, self.columns):
            x = offset_x + i * self.frame_width * self.thumbnail_scale_factor
            y_start = offset_y
            y_end = offset_y + self.scaled_thumbnail_spritesheet.get_height()
            pygame.draw.line(self.screen, self.RED, (x, y_start), (x, y_end), 1)
        
        # Draw horizontal lines
        for i in range(1, self.rows):
            y = offset_y + i * self.frame_height * self.thumbnail_scale_factor
            x_start = offset_x
            x_end = offset_x + self.scaled_thumbnail_spritesheet.get_width()
            pygame.draw.line(self.screen, self.RED, (x_start, y), (x_end, y), 1)
    
    def draw_current_frame_highlight(self, offset_x=0, offset_y=0):
        """Highlight the current frame on the thumbnail."""
        if not self.scaled_thumbnail_spritesheet:
            return
        
        col = self.current_frame % self.columns
        row = self.current_frame // self.columns
        
        x = offset_x + col * self.frame_width * self.thumbnail_scale_factor
        y = offset_y + row * self.frame_height * self.thumbnail_scale_factor
        width = self.frame_width * self.thumbnail_scale_factor
        height = self.frame_height * self.thumbnail_scale_factor
        
        pygame.draw.rect(self.screen, self.YELLOW, (x, y, width, height), 3)
    
    def draw_ui(self):
        """Draw the user interface"""
        panel = pygame.Rect(self.width - 380, 0, 380, self.height)
        pygame.draw.rect(self.screen, SURFACE, panel)
        pygame.draw.line(self.screen, BORDER, panel.topleft, panel.bottomleft)
        x, mouse = panel.x + 24, pygame.mouse.get_pos()
        text(self.screen, "PROBADOR", self.tiny_font, ACCENT, (x, 24))
        text(self.screen, "Previsualiza el movimiento", self.font, TEXT, (x, 44))
        name = os.path.basename(self.spritesheet_path) if self.spritesheet_path else "Ningún archivo seleccionado"
        text(self.screen, name[:40], self.small_font, MUTED, (x, 78))
        self.buttons = {"browse": pygame.Rect(x,108,332,42), "cols-":pygame.Rect(x,268,40,36), "cols+":pygame.Rect(x+126,268,40,36),
          "rows-":pygame.Rect(x+174,268,40,36), "rows+":pygame.Rect(x+292,268,40,36), "slow":pygame.Rect(x,332,48,38),
          "fast":pygame.Rect(x+284,332,48,38), "prev":pygame.Rect(x,404,72,44), "play":pygame.Rect(x+82,404,168,44),
          "next":pygame.Rect(x+260,404,72,44), "loop":pygame.Rect(x,474,158,40), "grid":pygame.Rect(x+174,474,158,40),
          "reset":pygame.Rect(x,530,158,38), "back":pygame.Rect(x+174,530,158,38)}
        button(self.screen,self.buttons["browse"],"Abrir spritesheet",self.button_font,mouse,primary=not self.spritesheet)
        info=pygame.Rect(x,168,332,76); rounded_panel(self.screen,info,BG,BORDER,12)
        stat(self.screen,x+14,181,"Imagen",f"{self.spritesheet.get_width()}×{self.spritesheet.get_height()}" if self.spritesheet else "—",self.tiny_font,font(16,True))
        stat(self.screen,x+126,181,"Cuadro",f"{self.frame_width}×{self.frame_height}" if self.spritesheet else "—",self.tiny_font,font(16,True))
        stat(self.screen,x+236,181,"Actual",f"{self.current_frame+1}/{self.total_frames}" if self.spritesheet else "—",self.tiny_font,font(16,True))
        enabled=bool(self.spritesheet)
        text(self.screen,"COLUMNAS",self.tiny_font,MUTED,(x+83,257),center=True)
        text(self.screen,str(self.columns),self.small_font,TEXT,(x+83,286),center=True)
        text(self.screen,"FILAS",self.tiny_font,MUTED,(x+257,257),center=True)
        text(self.screen,str(self.rows),self.small_font,TEXT,(x+257,286),center=True)
        for key,label in (("cols-","−"),("cols+","+"),("rows-","−"),("rows+","+")): button(self.screen,self.buttons[key],label,self.button_font,mouse,enabled=enabled)
        button(self.screen,self.buttons["slow"],"−",self.button_font,mouse,enabled=enabled); button(self.screen,self.buttons["fast"],"+",self.button_font,mouse,enabled=enabled)
        text(self.screen,f"Velocidad  {self.animation_speed} ms/cuadro",self.small_font,TEXT,(x+166,351),center=True)
        button(self.screen,self.buttons["prev"],"Anterior",self.tiny_font,mouse,enabled=enabled)
        button(self.screen,self.buttons["play"],"Pausar" if self.is_playing else "Reproducir",self.button_font,mouse,primary=enabled,enabled=enabled)
        button(self.screen,self.buttons["next"],"Siguiente",self.tiny_font,mouse,enabled=enabled)
        toggle_button(self.screen,self.buttons["loop"],"Repetir",self.button_font,self.tiny_font,mouse,self.loop,enabled)
        toggle_button(self.screen,self.buttons["grid"],"Cuadrícula",self.button_font,self.tiny_font,mouse,self.show_grid,enabled)
        button(self.screen,self.buttons["reset"],"Reiniciar",self.button_font,mouse,enabled=enabled)
        button(self.screen,self.buttons["back"],"Volver",self.button_font,mouse,enabled=True)
        text(self.screen,"Atajos",self.small_font,TEXT,(x,612)); text(self.screen,"Espacio reproducir · ← → navegar",self.small_font,MUTED,(x,642))
        text(self.screen,"Q/E columnas · A/D filas · Z/C velocidad",self.tiny_font,MUTED,(x,668)); text(self.screen,"B abrir · G cuadrícula · L repetir · Esc volver",self.tiny_font,MUTED,(x,692))
    
    def handle_input(self):
        """Handle keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.is_playing = not self.is_playing
                elif event.key == pygame.K_LEFT:
                    self.current_frame = max(0, self.current_frame - 1)
                elif event.key == pygame.K_RIGHT:
                    self.current_frame = min(self.total_frames - 1, self.current_frame + 1)
                elif event.key == pygame.K_q:  # Decrease columns
                    self.columns = max(1, self.columns - 1)
                    self.calculate_frame_dimensions()
                elif event.key == pygame.K_e:  # Increase columns
                    self.columns += 1
                    self.calculate_frame_dimensions()
                elif event.key == pygame.K_a:  # Decrease rows
                    self.rows = max(1, self.rows - 1)
                    self.calculate_frame_dimensions()
                elif event.key == pygame.K_d:  # Increase rows
                    self.rows += 1
                    self.calculate_frame_dimensions()
                elif event.key == pygame.K_z:  # Decrease speed
                    self.animation_speed = max(10, self.animation_speed - 10)
                elif event.key == pygame.K_c:  # Increase speed
                    self.animation_speed += 10
                elif event.key == pygame.K_l:  # Toggle loop
                    self.loop = not self.loop
                elif event.key == pygame.K_g:  # Toggle grid
                    self.show_grid = not self.show_grid
                elif event.key == pygame.K_r:  # Reset frame
                    self.current_frame = 0
                elif event.key == pygame.K_b:  # Browse spritesheet
                    self.browse_spritesheet()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                p=event.pos; hit=lambda key:self.buttons.get(key,pygame.Rect(0,0,0,0)).collidepoint(p)
                if hit("browse"): self.browse_spritesheet()
                elif hit("back"): return False
                elif self.spritesheet:
                    if hit("cols-"): self.columns=max(1,self.columns-1); self.calculate_frame_dimensions()
                    elif hit("cols+"): self.columns+=1; self.calculate_frame_dimensions()
                    elif hit("rows-"): self.rows=max(1,self.rows-1); self.calculate_frame_dimensions()
                    elif hit("rows+"): self.rows+=1; self.calculate_frame_dimensions()
                    elif hit("slow"): self.animation_speed=max(10,self.animation_speed-10)
                    elif hit("fast"): self.animation_speed+=10
                    elif hit("prev"): self.current_frame=max(0,self.current_frame-1); self.is_playing=False
                    elif hit("next"): self.current_frame=min(self.total_frames-1,self.current_frame+1); self.is_playing=False
                    elif hit("play"): self.is_playing=not self.is_playing
                    elif hit("loop"): self.loop=not self.loop
                    elif hit("grid"): self.show_grid=not self.show_grid
                    elif hit("reset"): self.current_frame=0
        
        return True
    
    def update_animation(self):
        """Update animation frame"""
        if not self.is_playing:
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_frame_time >= self.animation_speed:
            self.current_frame += 1
            self.last_frame_time = current_time
            
            if self.current_frame >= self.total_frames:
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = self.total_frames - 1
                    self.is_playing = False
    
    def draw(self):
        """Draw everything to the screen"""
        self.screen.fill(BG)
        
        # Draw animated frame in main view
        if self.spritesheet:
            animated_frame = self.get_frame_surface(self.current_frame, self.animation_scale_factor)
            if animated_frame:
                main_view_width = self.width - 380
                frame_rect = animated_frame.get_rect(center=(main_view_width / 2, self.height / 2))
                self.screen.blit(animated_frame, frame_rect)
        else:
            area=pygame.Rect(40,80,self.width-460,self.height-160); checkerboard(self.screen,area)
            rounded_panel(self.screen,pygame.Rect(area.centerx-230,area.centery-75,460,150),SURFACE,BORDER,18)
            text(self.screen,"Abre un spritesheet",font(24,True),TEXT,(area.centerx,area.centery-20),center=True)
            text(self.screen,"Selecciona un PNG y configura sus filas y columnas",self.small_font,MUTED,(area.centerx,area.centery+18),center=True)

        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def run(self, spritesheet_path=None):
        """Main game loop"""
        running = True
        
        # If a specific spritesheet is passed, load it
        if spritesheet_path and os.path.exists(spritesheet_path):
            self.load_spritesheet(spritesheet_path)
        # If no path was provided, remain empty until the user chooses a file.
        # This avoids unexpectedly auto-playing a colorful demo spritesheet.
        
        if not self.spritesheet:
            self.calculate_and_scale_assets()

        while running:
            # handle_input returns False to quit this tool
            if not self.handle_input():
                running = False 
            
            self.update_animation()
            self.draw()
            self.clock.tick(60)
        
        # When loop ends, just return to the main menu
        return

if __name__ == "__main__":
    # Ensure program receives focus on launch
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100, 100)
    tester = SpritesheetTester()
    tester.run()
