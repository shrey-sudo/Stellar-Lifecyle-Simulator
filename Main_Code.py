import pygame
import math
import random
import tkinter as tk
from tkinter import simpledialog

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ultimate Stellar Lifecycle Simulator")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
RED = (255, 69, 0)
BLUE = (70, 130, 180)
ORANGE = (255, 140, 0)
PURPLE = (138, 43, 226)
GRAY = (169, 169, 169)

# Font settings
font_title = pygame.font.Font(None, 45)
font_body = pygame.font.Font(None, 30)

# Stellar Lifecycle Paths Based on Mass
low_mass_path = [
    {"name": "Nebula", "color": BLUE, "size": 120, "brightness": 0.2},
    {"name": "Protostar", "color": ORANGE, "size": 100, "brightness": 0.5},
    {"name": "Main Sequence", "color": YELLOW, "size": 140, "brightness": 1.0},
    {"name": "Red Giant", "color": RED, "size": 200, "brightness": 1.5},
    {"name": "Planetary Nebula", "color": PURPLE, "size": 80, "brightness": 0.7},
    {"name": "White Dwarf", "color": GRAY, "size": 60, "brightness": 0.3}
]

neutron_star_path = [
    {"name": "Nebula", "color": BLUE, "size": 120, "brightness": 0.2},
    {"name": "Protostar", "color": ORANGE, "size": 100, "brightness": 0.5},
    {"name": "Main Sequence", "color": YELLOW, "size": 160, "brightness": 1.5},
    {"name": "Red Supergiant", "color": RED, "size": 220, "brightness": 2.0},
    {"name": "Supernova", "color": PURPLE, "size": 180, "brightness": 3.0},
    {"name": "Neutron Star", "color": GRAY, "size": 50, "brightness": 4.0}
]

black_hole_path = [
    {"name": "Nebula", "color": BLUE, "size": 120, "brightness": 0.2},
    {"name": "Protostar", "color": ORANGE, "size": 100, "brightness": 0.5},
    {"name": "Main Sequence", "color": YELLOW, "size": 160, "brightness": 1.5},
    {"name": "Red Supergiant", "color": RED, "size": 220, "brightness": 2.0},
    {"name": "Supernova", "color": PURPLE, "size": 180, "brightness": 3.0},
    {"name": "Black Hole/Neutron Star", "color": BLACK, "size": 40, "brightness": 5.0}
]

# Function to get user input for star mass using tkinter
def get_star_mass():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    try:
        mass = simpledialog.askfloat("Input", "Enter the mass of the star (in solar masses):")
        if mass is None:  # User canceled the input
            print("No input provided. Defaulting to 1 solar mass.")
            return 1.0
        return mass
    except ValueError:
        print("Invalid input. Defaulting to 1 solar mass.")
        return 1.0

# Get user input for star mass
star_mass = get_star_mass()

# Determine the stellar evolution path
if star_mass < 8:
    path = low_mass_path
elif 8 <= star_mass <= 20:
    path = neutron_star_path
elif star_mass > 20:
    path = black_hole_path
else:
    print("Invalid mass input. Defaulting to low-mass star.")
    path = low_mass_path

current_stage = 0
angle = 0

def next_stage():
    global current_stage
    current_stage = (current_stage + 1) % len(path)

running = True
explosion_particles = []

while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                next_stage()
                if path[current_stage]["name"] == "Supernova":
                    for _ in range(100):  # Generate explosion particles
                        explosion_particles.append([
                            WIDTH//2, HEIGHT//2, random.randint(-4, 4), random.randint(-4, 4), path[current_stage]["color"]
                        ])

    # Ensure current_stage is valid
    if 0 <= current_stage < len(path):
        stage = path[current_stage]
    else:
        print("Error: current_stage index out of bounds. Resetting to 0.")
        current_stage = 0
        stage = path[current_stage]

    # Draw current stellar stage
    pygame.draw.circle(screen, stage["color"], (WIDTH//2, HEIGHT//2), stage["size"])

    text_surface = font_title.render(stage["name"], True, WHITE)
    screen.blit(text_surface, (350, 600))

    # Stellar explosion effect (Supernova particles)
    for particle in explosion_particles:
        particle[0] += particle[2]  # Move x
        particle[1] += particle[3]  # Move y
        pygame.draw.circle(screen, particle[4], (particle[0], particle[1]), 3)

    # Accretion disk around black hole
    if stage["name"] == "Black Hole":
        for i in range(15):
            angle_offset = i * (math.pi / 7)
            disk_x = WIDTH//2 + int(60 * math.cos(angle + angle_offset))
            disk_y = HEIGHT//2 + int(20 * math.sin(angle + angle_offset))
            pygame.draw.circle(screen, GRAY, (disk_x, disk_y), 5)

    angle += 1  # Rotate planets and accretion disk

    pygame.display.flip()
    pygame.time.delay(50)

pygame.quit()
