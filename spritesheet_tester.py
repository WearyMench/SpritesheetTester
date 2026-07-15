import pygame
import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

class SpritesheetTester:
    def __init__(self, width=1200, height=800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Spritesheet Tester")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
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
        self.is_playing = True
        self.loop = True
        
        # UI properties
        self.thumbnail_scale_factor = 1.0
        self.animation_scale_factor = 3.0
        self.show_grid = True
        self.show_info = True
        
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
        # Background for UI
        ui_rect = pygame.Rect(self.width - 380, 0, 380, self.height)
        pygame.draw.rect(self.screen, self.GRAY, ui_rect)
        pygame.draw.rect(self.screen, self.WHITE, ui_rect, 2)
        
        y_offset = 20
        
        # Title
        title = self.font.render("Spritesheet Tester", True, self.BLACK)
        self.screen.blit(title, (self.width - 370, y_offset))
        y_offset += 40
        
        # File info
        if self.spritesheet_path:
            filename = os.path.basename(self.spritesheet_path)
            file_text = self.small_font.render(f"File: {filename}", True, self.BLACK)
            self.screen.blit(file_text, (self.width - 370, y_offset))
            y_offset += 25
            
            # Image dimensions
            dim_text = self.small_font.render(f"Image: {self.spritesheet.get_width()}x{self.spritesheet.get_height()}", True, self.BLACK)
            self.screen.blit(dim_text, (self.width - 370, y_offset))
            y_offset += 25
            
            # Frame dimensions
            frame_text = self.small_font.render(f"Frame: {self.frame_width}x{self.frame_height}", True, self.BLACK)
            self.screen.blit(frame_text, (self.width - 370, y_offset))
            y_offset += 25
            
            # Animation Scale factor
            scale_text = self.small_font.render(f"Anim Scale: {self.animation_scale_factor:.2f}x", True, self.BLACK)
            self.screen.blit(scale_text, (self.width - 370, y_offset))
            y_offset += 40

            # Spritesheet Thumbnail
            if self.scaled_thumbnail_spritesheet:
                thumb_x = self.width - 370
                thumb_y = y_offset
                self.screen.blit(self.scaled_thumbnail_spritesheet, (thumb_x, thumb_y))
                
                if self.show_grid:
                    self.draw_grid(thumb_x, thumb_y)
                
                self.draw_current_frame_highlight(thumb_x, thumb_y)
                
                y_offset += self.scaled_thumbnail_spritesheet.get_height() + 20
        
        # Controls
        controls_title = self.font.render("Controls:", True, self.BLACK)
        self.screen.blit(controls_title, (self.width - 370, y_offset))
        y_offset += 30
        
        # Columns and rows
        col_text = self.small_font.render(f"Columns: {self.columns} (Q/E)", True, self.BLACK)
        self.screen.blit(col_text, (self.width - 370, y_offset))
        y_offset += 20
        
        row_text = self.small_font.render(f"Rows: {self.rows} (A/D)", True, self.BLACK)
        self.screen.blit(row_text, (self.width - 370, y_offset))
        y_offset += 20
        
        # Animation speed
        speed_text = self.small_font.render(f"Speed: {self.animation_speed}ms (Z/C)", True, self.BLACK)
        self.screen.blit(speed_text, (self.width - 370, y_offset))
        y_offset += 20
        
        # Current frame
        frame_text = self.small_font.render(f"Frame: {self.current_frame + 1}/{self.total_frames}", True, self.BLACK)
        self.screen.blit(frame_text, (self.width - 370, y_offset))
        y_offset += 20
        
        # Play/pause
        play_text = self.small_font.render(f"Playing: {'Yes' if self.is_playing else 'No'} (Space)", True, self.BLACK)
        self.screen.blit(play_text, (self.width - 370, y_offset))
        y_offset += 20
        
        # Loop
        loop_text = self.small_font.render(f"Loop: {'Yes' if self.loop else 'No'} (L)", True, self.BLACK)
        self.screen.blit(loop_text, (self.width - 370, y_offset))
        y_offset += 20
        
        # Grid toggle
        grid_text = self.small_font.render(f"Grid: {'On' if self.show_grid else 'Off'} (G)", True, self.BLACK)
        self.screen.blit(grid_text, (self.width - 370, y_offset))
        y_offset += 40
        
        # Instructions
        instructions = [
            "SPACE - Play/Pause",
            "LEFT/RIGHT - Previous/Next frame",
            "Q/E - Change columns",
            "A/D - Change rows",
            "Z/C - Change speed",
            "L - Toggle loop",
            "G - Toggle grid",
            "R - Reset frame",
            "B - Browse spritesheet",
            "ESC - Quit"
        ]
        
        for instruction in instructions:
            inst_text = self.small_font.render(instruction, True, self.BLACK)
            self.screen.blit(inst_text, (self.width - 370, y_offset))
            y_offset += 20
    
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
        self.screen.fill(self.BLACK)
        
        # Draw animated frame in main view
        if self.spritesheet:
            animated_frame = self.get_frame_surface(self.current_frame, self.animation_scale_factor)
            if animated_frame:
                main_view_width = self.width - 380
                frame_rect = animated_frame.get_rect(center=(main_view_width / 2, self.height / 2))
                self.screen.blit(animated_frame, frame_rect)
        else:
            font = pygame.font.Font(None, 36)
            small_font = pygame.font.Font(None, 24)
            
            # Main message
            text = font.render("No spritesheet loaded", True, self.WHITE)
            text_rect = text.get_rect(center=((self.width - 380) / 2, self.height / 2 - 30))
            self.screen.blit(text, text_rect)
            
            # Instructions
            instruction_text = small_font.render("Press B to browse for a spritesheet image", True, self.GRAY)
            instruction_rect = instruction_text.get_rect(center=((self.width - 380) / 2, self.height / 2 + 10))
            self.screen.blit(instruction_text, instruction_rect)

        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def run(self, spritesheet_path=None):
        """Main game loop"""
        running = True
        
        # If a specific spritesheet is passed, load it
        if spritesheet_path and os.path.exists(spritesheet_path):
            self.load_spritesheet(spritesheet_path)
        else:
            # Try to load a default spritesheet if available
            default_paths = ["spritesheet.png", "sprite.png", "test.png"]
            for path in default_paths:
                if os.path.exists(path):
                    self.load_spritesheet(path)
                    break
        
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