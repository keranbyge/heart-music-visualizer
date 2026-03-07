import pygame
import math
import subprocess
import sys
import time

# Initialize pygame
pygame.init()

# Window setup
WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Heart Animation")
clock = pygame.time.Clock()

# Load lyrics
def load_lyrics(filename):
    lyrics = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                parts = line.strip().split(None, 1)
                if len(parts) == 2:
                    lyrics.append((float(parts[0]), parts[1]))
    except FileNotFoundError:
        pass
    return sorted(lyrics)

lyrics = load_lyrics("lyrics.txt")

# Start music and timer
music_process = subprocess.Popen(["afplay", "song.mp3"])
start_time = time.time()

# Generate heart points
def generate_heart_points(num_points=200):
    points = []
    for i in range(num_points):
        t = (i / num_points) * 2 * math.pi
        x = 16 * math.sin(t)**3
        y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
        screen_x = WIDTH // 2 + x * 16
        screen_y = HEIGHT // 2 - y * 16
        points.append((screen_x, screen_y))
    return points

points = generate_heart_points(200)

# Get current lyric
def get_current_lyric(elapsed_time):
    current = ""
    for timestamp, text in lyrics:
        if elapsed_time >= timestamp:
            current = text
        else:
            break
    return current

# Font setup
font = pygame.font.Font(None, 60)

# Animation parameters
rotation_angle = 0
prev_lyric = ""
lyric_alpha = 0
target_alpha = 180

# Main loop
running = True
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get elapsed time
        elapsed_time = time.time() - start_time
        current_lyric = get_current_lyric(elapsed_time)
        
        # Fade logic
        if current_lyric != prev_lyric:
            lyric_alpha = 0
            prev_lyric = current_lyric
        elif lyric_alpha < target_alpha:
            lyric_alpha = min(lyric_alpha + 5, target_alpha)
        
        # Black background
        screen.fill((0, 0, 0))
        
        # Draw lyrics behind heart
        if current_lyric:
            text_surface = font.render(current_lyric, True, (255, 255, 255))
            text_with_alpha = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
            text_surface.set_alpha(lyric_alpha)
            text_with_alpha.blit(text_surface, (0, 0))
            text_rect = text_with_alpha.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_with_alpha, text_rect)
        
        # Draw rotating spiral heart
        line_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        
        # Multiple spiral layers for depth
        for layer in range(3):
            offset = int(rotation_angle + layer * 30) % len(points)
            step = max(1, len(points) // 40)
            
            for i in range(0, len(points), step):
                start_idx = i
                end_idx = (i + offset) % len(points)
                
                # Glow effect with varying alpha
                alpha = 60 + layer * 20
                color = (255, 30 + layer * 30, 30 + layer * 30, alpha)
                
                pygame.draw.line(line_surface, color, 
                               points[start_idx], points[end_idx], 2)
        
        # Additional connecting lines for density
        for i in range(0, len(points), 3):
            j = (i + int(rotation_angle * 2)) % len(points)
            pygame.draw.line(line_surface, (255, 80, 80, 40), 
                           points[i], points[j], 1)
        
        screen.blit(line_surface, (0, 0))
        
        # Update rotation (only until all lyrics are shown)
        if lyrics and elapsed_time < lyrics[-1][0]:
            rotation_angle += 0.3
        
        pygame.display.flip()
        clock.tick(60)

finally:
    # Stop music when animation finishes or window closes
    music_process.terminate()
    pygame.quit()
    sys.exit()
