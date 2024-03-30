# import pygame
# import sys

# # Initialize Pygame
# pygame.init()

# # Constants
# SCREEN_WIDTH = 800
# SCREEN_HEIGHT = 600
# BIRD_SIZE = 40
# BIRD_COLOR = (255, 255, 0)  # Yellow
# BACKGROUND_COLOR = (135, 206, 235)  # Sky Blue
# GRAVITY = 0.5
# FLAP_STRENGTH = 10

# # Create the screen
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Flappy Bird")

# # Bird class
# class Bird:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.velocity = 0

#     def flap(self):
#         self.velocity = -FLAP_STRENGTH

#     def update(self):
#         self.velocity += GRAVITY
#         self.y += self.velocity

#     def draw(self):
#         pygame.draw.circle(screen, BIRD_COLOR, (self.x, int(self.y)), BIRD_SIZE // 2)

# # Background class
# class Background:
#     def __init__(self):
#         self.image = pygame.image.load("background.png").convert()
#         self.rect = self.image.get_rect()

#     def draw(self):
#         screen.blit(self.image, self.rect)

# # Main function
# def main():
#     bird = Bird(100, SCREEN_HEIGHT // 2)
#     background = Background()

#     clock = pygame.time.Clock()

#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_SPACE:
#                     bird.flap()

#         bird.update()

#         screen.fill(BACKGROUND_COLOR)
#         background.draw()
#         bird.draw()

#         pygame.display.flip()
#         clock.tick(60)

# if __name__ == "__main__":
#     main()
import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BIRD_SIZE = 40
PIPE_WIDTH = 50
PIPE_GAP = 200
PIPE_SPEED = 5
BIRD_COLOR = (255, 255, 0)  # Yellow
PIPE_COLOR = (0, 128, 0)     # Green
BACKGROUND_COLOR = (135, 206, 235)  # Sky Blue
GRAVITY = 0.5
FLAP_STRENGTH = 10

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Bird class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0

    def flap(self):
        self.velocity = -FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        pygame.draw.circle(screen, BIRD_COLOR, (self.x, int(self.y)), BIRD_SIZE // 2)

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self):
        top_pipe_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.gap_y)
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - (self.gap_y + PIPE_GAP))
        pygame.draw.rect(screen, PIPE_COLOR, top_pipe_rect)
        pygame.draw.rect(screen, PIPE_COLOR, bottom_pipe_rect)

# Background class
class Background:
    def __init__(self):
        self.image = pygame.image.load("background.png").convert()
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, self.rect)

# Main function
def main():
    bird = Bird(100, SCREEN_HEIGHT // 2)
    background = Background()
    pipes = []

    clock = pygame.time.Clock()
    frame_count = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()

        bird.update()

        # Add pipes
        frame_count += 1
        if frame_count % 100 == 0:
            new_pipe = Pipe(SCREEN_WIDTH)
            pipes.append(new_pipe)

        # Update pipes
        for pipe in pipes:
            pipe.move()

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

        screen.fill(BACKGROUND_COLOR)
        background.draw()
        bird.draw()

        for pipe in pipes:
            pipe.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
