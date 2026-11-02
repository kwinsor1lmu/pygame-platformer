import pygame
import sys

# --- Configuration ---
WIDTH, HEIGHT = 800, 400
FPS = 60
GRAVITY = 0.8
JUMP_STRENGTH = -15
SPEED = 5

# Colors
WHITE = (255, 255, 255)
GRAY  = (180, 180, 180)
RED   = (255, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# --- Objects ---
player = pygame.Rect(50, 250, 30, 30)
player_vel_y = 0
on_ground = False

# Platforms (x, y, width, height)
platforms = [
    pygame.Rect(0, 350, 150, 50),     # Starting block
    pygame.Rect(200, 280, 100, 20),   # Floating platform
    pygame.Rect(450, 320, 120, 20),   # Lower middle
    pygame.Rect(600, 220, 80, 15),    # High right
]

# Hazards (Spikes) - Represented as triangles
# Format: (Point1, Point2, Point3)
spikes = [
    [(320, 300), (340, 300), (330, 270)], # Simple floor spike
    [(600, 100), (640, 100), (620, 130)]  # Ceiling spike
]

def reset_player():
    global player_vel_y
    player.x, player.y = 50, 250
    player_vel_y = 0

# --- Main Loop ---
while True:
    screen.fill(GRAY)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and on_ground:
                player_vel_y = JUMP_STRENGTH
                on_ground = False

    # Movement: Check which keys are currently held down
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:  # Move left + boundary check
        player.x -= SPEED
    if keys[pygame.K_RIGHT] and player.right < WIDTH:  # Move right + boundary check
        player.x += SPEED

    # Physics: Gravity
    previous_bottom = player.bottom
    player_vel_y += GRAVITY
    player.y += player_vel_y

    # Collision: Platforms
    # Only land if the player was above the platform, so hitting its side
    # doesn't teleport them on top. The 1px offset keeps on_ground steady
    # while standing still.
    on_ground = False
    for plat in platforms:
        if player_vel_y >= 0 and previous_bottom <= plat.top and player.move(0, 1).colliderect(plat):
            player.bottom = plat.top
            player_vel_y = 0
            on_ground = True

    # Collision: Spikes (Simplistic point-in-rect check)
    for spike in spikes:
        spike_rect = pygame.draw.polygon(screen, BLACK, spike)
        if player.colliderect(spike_rect):
            reset_player()

    # Draw Platforms
    for plat in platforms:
        pygame.draw.rect(screen, WHITE, plat)
        pygame.draw.rect(screen, BLACK, plat, 2) # Outline

    # Draw Player
    pygame.draw.rect(screen, RED, player)
    pygame.draw.rect(screen, BLACK, player, 2)

    # Screen Wrap/Fall off
    if player.y > HEIGHT:
        reset_player()

    pygame.display.flip()
    clock.tick(FPS)