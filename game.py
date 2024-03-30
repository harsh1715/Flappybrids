import pygame
import sys
import random
import numpy as np
from pygame.locals import *

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
BLUR_RADIUS = 15  # Blur radius for optic lens effect

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Bird class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.radius = BIRD_SIZE // 2

    def flap(self):
        self.velocity = -FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        pygame.draw.circle(screen, BIRD_COLOR, (self.x, int(self.y)), self.radius)

    def get_pos(self):
        return np.array([self.x, self.y])

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_y = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.pipe_width = PIPE_WIDTH
        self.pipe_gap = PIPE_GAP

    def move(self):
        self.x -= PIPE_SPEED

    def draw(self):
        top_pipe_rect = pygame.Rect(self.x, 0, self.pipe_width, self.gap_y)
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + self.pipe_gap, self.pipe_width, SCREEN_HEIGHT - (self.gap_y + self.pipe_gap))
        pygame.draw.rect(screen, PIPE_COLOR, top_pipe_rect)
        pygame.draw.rect(screen, PIPE_COLOR, bottom_pipe_rect)

    def get_rects(self):
        top_pipe_rect = pygame.Rect(self.x, 0, self.pipe_width, self.gap_y)
        bottom_pipe_rect = pygame.Rect(self.x, self.gap_y + self.pipe_gap, self.pipe_width, SCREEN_HEIGHT - (self.gap_y + self.pipe_gap))
        return top_pipe_rect, bottom_pipe_rect

# Background class
class Background:
    def __init__(self):
        self.image = pygame.image.load("background.png").convert()
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, self.rect)

# Button class for start button
class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.text_render = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_render.get_rect(center=self.rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_render, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Check collision between bird and pipes
def check_collision(bird, pipes):
    bird_pos = bird.get_pos()
    bird_radius = bird.radius
    for pipe in pipes:
        top_pipe_rect, bottom_pipe_rect = pipe.get_rects()
        
        # Check collision with top pipe
        if circle_rect_collision(bird_pos, bird_radius, top_pipe_rect):
            return True
        # Check collision with bottom pipe
        if circle_rect_collision(bird_pos, bird_radius, bottom_pipe_rect):
            return True
    return False

# Function to check collision between a circle (bird) and a rectangle (pipe)
def circle_rect_collision(circle_pos, circle_radius, rect):
    closest_x = max(rect.left, min(circle_pos[0], rect.right))
    closest_y = max(rect.top, min(circle_pos[1], rect.bottom))
    distance_squared = (circle_pos[0] - closest_x) ** 2 + (circle_pos[1] - closest_y) ** 2
    return distance_squared < circle_radius ** 2

# Apply blur optic lens effect
def apply_blur_effect(surface, radius):
    rect = surface.get_rect()
    sub = surface.subsurface(rect)
    sub = pygame.transform.smoothscale(sub, (rect.width // 10, rect.height // 10))
    sub = pygame.transform.smoothscale(sub, (rect.width, rect.height))
    sub.set_alpha(150)
    surface.blit(sub, rect)

# Main function
def main():
    bird = Bird(100, SCREEN_HEIGHT // 2)
    background = Background()
    pipes = []
    start_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2, 100, 50, (0, 0, 255), "Start")

    clock = pygame.time.Clock()
    frame_count = 0
    game_over = False
    game_started = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_started:
                        bird.flap()
                    else:
                        game_started = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.is_clicked(mouse_pos):
                        game_started = True

        if game_started:
            bird.update()

            # Exit game if bird drops below the screen
            if bird.y + bird.radius > SCREEN_HEIGHT:
                game_over = True

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

            # Check collision
            if check_collision(bird, pipes):
                game_over = True

        screen.fill(BACKGROUND_COLOR)
        background.draw()
        bird.draw()

        for pipe in pipes:
            pipe.draw()

        # Apply blur effect if game hasn't started
        if not game_started:
            apply_blur_effect(screen, BLUR_RADIUS)
            start_button.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
 