import pygame
import math
import random


# Initialize Pygame
pygame.init()

# Game Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)

# Screen Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Archery Game")
clock = pygame.time.Clock()

# Load Arrow Image
arrow_img = pygame.image.load("arrow.png")
arrow_img = pygame.transform.scale(arrow_img, (40, 10))

# Target Setup
target_radius = 30


def draw_target(target_x, target_y, target_radius):
    """Draws the target on the screen."""
    pygame.draw.circle(screen, RED, (target_x, target_y), target_radius)


def calculate_distance(x1, y1, x2, y2):
    """Calculates the distance between two points."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def main():
    """Main game loop."""
    running = True
    target_x = random.randint(400, 750)
    target_y = random.randint(100, 500)
    arrow_x, arrow_y = 100, HEIGHT // 2  # Initial arrow position
    angle = 0  # Shooting angle
    shooting = False  # Shooting status
    velocity = 0  # Arrow velocity
    hit = False  # Hit detection

    while running:
        screen.fill(WHITE)
        draw_target(target_x, target_y, target_radius)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    angle -= 5
                elif event.key == pygame.K_DOWN:
                    angle += 5
                elif event.key == pygame.K_SPACE and not shooting:
                    shooting = True
                    velocity = 15

        if shooting:
            arrow_x += velocity * math.cos(math.radians(angle))
            arrow_y -= velocity * math.sin(math.radians(angle))

            if calculate_distance(
                arrow_x, arrow_y, target_x, target_y
            ) < target_radius:
                hit = True
                shooting = False
                print("Hit!")
            elif arrow_x > WIDTH or arrow_y < 0 or arrow_y > HEIGHT:
                shooting = False
                arrow_x, arrow_y = 100, HEIGHT // 2

        rotated_arrow = pygame.transform.rotate(arrow_img, -angle)
        screen.blit(rotated_arrow, (arrow_x, arrow_y))
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()
