import pygame
import sys
import os

def create_test_spritesheet():
    """Create a simple test spritesheet with colored squares"""
    pygame.init()
    
    # Spritesheet dimensions
    frame_size = 64
    columns = 4
    rows = 4
    width = frame_size * columns
    height = frame_size * rows
    
    # Create surface
    spritesheet = pygame.Surface((width, height))
    spritesheet.fill((255, 255, 255))  # White background
    
    # Colors for different frames
    colors = [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (255, 128, 0),  # Orange
        (128, 0, 255),  # Purple
        (0, 128, 0),    # Dark Green
        (128, 128, 128), # Gray
        (255, 192, 203), # Pink
        (165, 42, 42),   # Brown
        (255, 215, 0),   # Gold
        (0, 128, 128),   # Teal
        (128, 0, 128),   # Dark Purple
        (255, 165, 0),   # Orange
    ]
    
    # Draw frames
    for row in range(rows):
        for col in range(columns):
            frame_index = row * columns + col
            if frame_index < len(colors):
                color = colors[frame_index]
            else:
                color = (100, 100, 100)  # Default gray
            
            # Calculate position
            x = col * frame_size
            y = row * frame_size
            
            # Draw colored rectangle
            pygame.draw.rect(spritesheet, color, (x, y, frame_size, frame_size))
            
            # Draw frame number
            font = pygame.font.Font(None, 24)
            text = font.render(str(frame_index + 1), True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + frame_size // 2, y + frame_size // 2))
            spritesheet.blit(text, text_rect)
            
            # Draw border
            pygame.draw.rect(spritesheet, (0, 0, 0), (x, y, frame_size, frame_size), 2)
    
    # Save the spritesheet
    pygame.image.save(spritesheet, "spritesheet.png")
    print(f"Created test spritesheet: spritesheet.png ({width}x{height})")
    print(f"Frame size: {frame_size}x{frame_size}")
    print(f"Grid: {columns}x{rows} = {columns * rows} frames")
    
    pygame.quit()

if __name__ == "__main__":
    create_test_spritesheet() 