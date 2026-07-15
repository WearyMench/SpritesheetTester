import pygame
import sys
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from pathlib import Path

class SpritesheetCreator:
    def __init__(self):
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Spritesheet Creator")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        
        # Initialize tkinter for file dialogs
        self.tk_root = tk.Tk()
        self.tk_root.withdraw()
        
        # Image list and properties
        self.images = []
        self.image_paths = []
        self.columns = 4
        self.rows = 4
        self.frame_width = 64
        self.frame_height = 64
        self.background_color = (255, 255, 255)  # White
        
        # Preview & Resizing properties
        self.preview_spritesheet = None
        self.final_spritesheet = None
        self.output_width = 0
        self.output_height = 0
        self.aspect_ratio_locked = True
        self.original_aspect_ratio = 1.0
        
        # Preview properties
        self.show_grid = True
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255, 255, 0)
        self.LIGHT_GRAY = (200, 200, 200)
        self.LIGHT_BLUE = (173, 216, 230)
        self.DARK_BLUE = (0, 0, 139)
        
    def browse_images(self):
        """Open file dialog to select multiple images"""
        try:
            filetypes = [
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.tga"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("All files", "*.*")
            ]
            
            file_paths = filedialog.askopenfilenames(
                title="Select Images for Spritesheet",
                filetypes=filetypes,
                initialdir=os.getcwd()
            )
            
            if file_paths:
                self.load_images(file_paths)
                return True
        except Exception as e:
            messagebox.showerror("Error", f"Error browsing files:\n{str(e)}")
        
        return False
    
    def load_images(self, file_paths):
        """Load multiple images from file paths"""
        self.images = []
        self.image_paths = []
        
        for path in file_paths:
            try:
                abs_path = os.path.abspath(path)
                image = pygame.image.load(abs_path)
                self.images.append(image)
                self.image_paths.append(abs_path)
                print(f"Loaded: {os.path.basename(abs_path)}")
            except pygame.error as e:
                print(f"Error loading {path}: {e}")
        
        if self.images:
            self.calculate_grid_size()
            self.create_preview()
            print(f"Loaded {len(self.images)} images")
    
    def calculate_grid_size(self):
        """Calculate optimal grid size based on number of images"""
        if not self.images:
            return
        
        num_images = len(self.images)
        
        # Try to find a good grid size
        if num_images <= 4:
            self.columns = num_images
            self.rows = 1
        elif num_images <= 8:
            self.columns = 4
            self.rows = 2
        elif num_images <= 12:
            self.columns = 4
            self.rows = 3
        elif num_images <= 16:
            self.columns = 4
            self.rows = 4
        elif num_images <= 20:
            self.columns = 5
            self.rows = 4
        elif num_images <= 25:
            self.columns = 5
            self.rows = 5
        else:
            # For larger sets, calculate approximately square grid
            import math
            self.columns = math.ceil(math.sqrt(num_images))
            self.rows = math.ceil(num_images / self.columns)
    
    def create_preview(self):
        """Create a preview of the spritesheet"""
        if not self.images:
            return
        
        # Calculate frame size based on largest image
        max_width = max(img.get_width() for img in self.images)
        max_height = max(img.get_height() for img in self.images)
        
        # Use the larger dimension to ensure all images fit
        self.frame_width = max_width
        self.frame_height = max_height
        
        # Create spritesheet surface with transparency
        spritesheet_width = self.columns * self.frame_width
        spritesheet_height = self.rows * self.frame_height
        
        self.preview_spritesheet = pygame.Surface((spritesheet_width, spritesheet_height), pygame.SRCALPHA)
        self.preview_spritesheet.fill((0, 0, 0, 0))  # Fill with transparent color
        
        # Place images in grid
        for i, image in enumerate(self.images):
            if i >= self.columns * self.rows:
                break
            
            col = i % self.columns
            row = i // self.columns
            
            x = col * self.frame_width
            y = row * self.frame_height
            
            # Center the image in its frame
            img_rect = image.get_rect()
            img_rect.center = (x + self.frame_width // 2, y + self.frame_height // 2)
            
            self.preview_spritesheet.blit(image, img_rect)
            
        # Set initial output size
        self.reset_output_size()
    
    def reset_output_size(self):
        """Resets the output size to the original preview size."""
        if self.preview_spritesheet:
            self.final_spritesheet = self.preview_spritesheet
            w = self.preview_spritesheet.get_width()
            h = self.preview_spritesheet.get_height()
            self.output_width = w
            self.output_height = h
            if h > 0:
                self.original_aspect_ratio = w / h
    
    def resize_final_spritesheet(self, new_width, new_height):
        """Resizes the final spritesheet using the preview as a source."""
        if self.preview_spritesheet:
            self.output_width = max(1, int(new_width))
            self.output_height = max(1, int(new_height))
            self.final_spritesheet = pygame.transform.smoothscale(
                self.preview_spritesheet, (self.output_width, self.output_height)
            )

    def save_spritesheet(self):
        """Save the current spritesheet"""
        if not self.final_spritesheet:
            messagebox.showwarning("Warning", "No spritesheet to save!")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="Save Spritesheet",
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")],
                initialdir=os.getcwd(),
                initialfile="spritesheet.png"
            )
            
            if file_path:
                pygame.image.save(self.final_spritesheet, file_path)
                messagebox.showinfo("Success", f"Spritesheet saved as:\n{file_path}")
                print(f"Spritesheet saved: {file_path}")
                return file_path
        except Exception as e:
            messagebox.showerror("Error", f"Error saving spritesheet:\n{str(e)}")
        
        return None
    
    def set_grid_size(self):
        """Set custom grid size"""
        try:
            cols = simpledialog.askinteger("Grid Size", "Number of columns:", 
                                         initialvalue=self.columns, minvalue=1, maxvalue=20)
            if cols is not None:
                rows = simpledialog.askinteger("Grid Size", "Number of rows:", 
                                             initialvalue=self.rows, minvalue=1, maxvalue=20)
                if rows is not None:
                    self.columns = cols
                    self.rows = rows
                    self.create_preview()
        except Exception as e:
            messagebox.showerror("Error", f"Error setting grid size:\n{str(e)}")
    
    def prompt_for_output_size(self):
        """Prompt user for new output dimensions."""
        if not self.preview_spritesheet:
            messagebox.showwarning("Warning", "Load images first!")
            return

        try:
            new_width, new_height = None, None

            if self.aspect_ratio_locked:
                # Ask the user which dimension they want to set
                resize_by_width = messagebox.askquestion(
                    "Resize Method",
                    "Do you want to set the WIDTH and calculate height automatically?\n\n(Choose 'No' to set the HEIGHT instead)"
                )

                if resize_by_width == 'yes':
                    new_width_str = simpledialog.askstring("Resize by Width", "Enter new width (pixels):",
                                                           initialvalue=str(self.output_width))
                    if new_width_str is None: return
                    new_width = int(new_width_str)
                    new_height = int(new_width / self.original_aspect_ratio)
                else: # 'no'
                    new_height_str = simpledialog.askstring("Resize by Height", "Enter new height (pixels):",
                                                            initialvalue=str(self.output_height))
                    if new_height_str is None: return
                    new_height = int(new_height_str)
                    new_width = int(new_height * self.original_aspect_ratio)

            else: # Aspect ratio is unlocked
                new_width_str = simpledialog.askstring("Resize Output", "Enter new width (pixels):",
                                                        initialvalue=str(self.output_width))
                if new_width_str is None: return
                new_width = int(new_width_str)

                new_height_str = simpledialog.askstring("Resize Output", "Enter new height (pixels):",
                                                        initialvalue=str(self.output_height))
                if new_height_str is None: return
                new_height = int(new_height_str)
            
            if new_width is not None and new_height is not None:
                self.resize_final_spritesheet(new_width, new_height)

        except (ValueError, TypeError) as e:
            messagebox.showerror("Error", f"Invalid input. Please enter numbers only.\n{e}")

    def draw_ui(self):
        """Draw the user interface"""
        # Background for UI
        ui_rect = pygame.Rect(self.width - 380, 0, 380, self.height)
        pygame.draw.rect(self.screen, self.GRAY, ui_rect)
        pygame.draw.rect(self.screen, self.WHITE, ui_rect, 2)
        
        y_offset = 20
        
        # Title
        title = self.font.render("Spritesheet Creator", True, self.BLACK)
        self.screen.blit(title, (self.width - 370, y_offset))
        y_offset += 40
        
        # Image count
        count_text = self.small_font.render(f"Images loaded: {len(self.images)}", True, self.BLACK)
        self.screen.blit(count_text, (self.width - 370, y_offset))
        y_offset += 25
        
        # Grid info
        if self.images:
            grid_text = self.small_font.render(f"Grid: {self.columns}x{self.rows}", True, self.BLACK)
            self.screen.blit(grid_text, (self.width - 370, y_offset))
            y_offset += 25
            
            frame_text = self.small_font.render(f"Frame size: {self.frame_width}x{self.frame_height}", True, self.BLACK)
            self.screen.blit(frame_text, (self.width - 370, y_offset))
            y_offset += 25
            
            total_text = self.small_font.render(f"Total frames: {self.columns * self.rows}", True, self.BLACK)
            self.screen.blit(total_text, (self.width - 370, y_offset))
            y_offset += 25

            # --- RESIZE SECTION ---
            resize_title = self.font.render("Output Resizing:", True, self.BLACK)
            self.screen.blit(resize_title, (self.width - 370, y_offset))
            y_offset += 30

            # Display output dimensions
            output_dim_text = self.small_font.render(f"Size: {self.output_width}x{self.output_height}", True, self.BLACK)
            self.screen.blit(output_dim_text, (self.width - 370, y_offset))
            y_offset += 25

            # Aspect ratio status
            aspect_status = "Locked" if self.aspect_ratio_locked else "Unlocked"
            aspect_text = self.small_font.render(f"Aspect Ratio: {aspect_status}", True, self.BLACK)
            self.screen.blit(aspect_text, (self.width - 370, y_offset))
            y_offset += 40
        
        # Controls
        controls_title = self.font.render("Controls:", True, self.BLACK)
        self.screen.blit(controls_title, (self.width - 370, y_offset))
        y_offset += 30
        
        # Control options
        controls = [
            "B - Browse images",
            "G - Set grid size",
            "R - Resize output",
            "L - Lock/Unlock aspect ratio",
            "X - Reset size",
            "S - Save spritesheet",
            "T - Test spritesheet",
            "C - Clear images",
            "ESC - Quit"
        ]
        
        for control in controls:
            control_text = self.small_font.render(control, True, self.BLACK)
            self.screen.blit(control_text, (self.width - 370, y_offset))
            y_offset += 20
        
        y_offset += 20
        
        # Instructions
        instructions = [
            "1. Press B to select images",
            "2. Adjust grid size if needed",
            "3. Press R to resize output",
            "4. Press L to lock/unlock aspect ratio",
            "5. Press X to reset size",
            "6. Press S to save spritesheet",
            "7. Press T to test animation"
        ]
        
        for instruction in instructions:
            inst_text = self.small_font.render(instruction, True, self.BLACK)
            self.screen.blit(inst_text, (self.width - 370, y_offset))
            y_offset += 20
    
    def draw_preview(self):
        """Draw the spritesheet preview"""
        if self.final_spritesheet:
            # Scale preview to fit main area
            preview_width = self.width - 400
            preview_height = self.height - 100
            
            w = self.final_spritesheet.get_width()
            h = self.final_spritesheet.get_height()
            
            if w == 0 or h == 0: return

            scale_x = preview_width / w
            scale_y = preview_height / h
            scale = min(scale_x, scale_y, 2.0)  # Max scale of 2x
            
            scaled_width = int(w * scale)
            scaled_height = int(h * scale)
            
            scaled_preview = pygame.transform.scale(self.final_spritesheet, (scaled_width, scaled_height))
            
            # Center the preview
            x = (preview_width - scaled_width) // 2
            y = (self.height - scaled_height) // 2
            
            self.screen.blit(scaled_preview, (x, y))
            
            # Draw grid if enabled
            if self.show_grid:
                self.draw_grid(x, y, scale)
        else:
            # Show placeholder
            font = pygame.font.Font(None, 36)
            text = font.render("No spritesheet preview", True, self.WHITE)
            text_rect = text.get_rect(center=((self.width - 380) // 2, self.height // 2))
            self.screen.blit(text, text_rect)
    
    def draw_grid(self, offset_x, offset_y, scale):
        """Draw grid lines on the preview"""
        if not self.final_spritesheet:
            return
        
        # Draw vertical lines
        for i in range(1, self.columns):
            x = offset_x + i * self.frame_width * scale
            y_start = offset_y
            y_end = offset_y + self.final_spritesheet.get_height() * scale
            pygame.draw.line(self.screen, self.RED, (x, y_start), (x, y_end), 1)
        
        # Draw horizontal lines
        for i in range(1, self.rows):
            y = offset_y + i * self.frame_height * scale
            x_start = offset_x
            x_end = offset_x + self.final_spritesheet.get_width() * scale
            pygame.draw.line(self.screen, self.RED, (x_start, y), (x_end, y), 1)
    
    def handle_input(self):
        """Handle keyboard input. Returns False to quit, or a path to test."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_b:  # Browse images
                    self.browse_images()
                elif event.key == pygame.K_g:  # Set grid size
                    self.set_grid_size()
                elif event.key == pygame.K_r: # Resize
                    self.prompt_for_output_size()
                elif event.key == pygame.K_l: # Lock aspect ratio
                    self.aspect_ratio_locked = not self.aspect_ratio_locked
                elif event.key == pygame.K_x: # Reset size
                    self.reset_output_size()
                elif event.key == pygame.K_s:  # Save spritesheet
                    self.save_spritesheet()
                elif event.key == pygame.K_t:  # Test spritesheet
                    if self.final_spritesheet:
                        # Create temp directory if it doesn't exist
                        temp_dir = os.path.join(os.getcwd(), "temp")
                        if not os.path.exists(temp_dir):
                            os.makedirs(temp_dir)

                        # Save temporary file and return its path for testing
                        temp_path = os.path.join(temp_dir, "temp_spritesheet_for_testing.png")
                        pygame.image.save(self.final_spritesheet, temp_path)
                        return temp_path
                    else:
                        messagebox.showwarning("Warning", "No spritesheet to test!")
                elif event.key == pygame.K_c:  # Clear images
                    self.images = []
                    self.image_paths = []
                    self.preview_spritesheet = None
                    self.final_spritesheet = None
                    print("Images cleared")
        
        return True
    
    def test_spritesheet(self, spritesheet_path):
        """This method is now obsolete in the integrated GUI. 
           The main loop handles launching the tester."""
        print("Testing is now handled by the main application loop.")
    
    def draw(self):
        """Draw everything to the screen"""
        self.screen.fill(self.BLACK)
        
        # Draw preview
        self.draw_preview()
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # handle_input can return a path to test or False to quit
            result = self.handle_input()
            if result is False:
                running = False
            elif isinstance(result, str) and result.endswith('.png'):
                # This is a path to a spritesheet to be tested
                return {"action": "test", "path": result}

            self.draw()
            self.clock.tick(60)
        
        # When loop ends, just return to the main menu
        return {"action": "menu"}

if __name__ == "__main__":
    creator = SpritesheetCreator()
    creator.run() 