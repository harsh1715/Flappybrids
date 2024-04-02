import pygame
import sys
import random
import numpy as np
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BIRD_SIZE = 40
PIPE_WIDTH = 50
PIPE_GAP = 200
PIPE_SPEED = 5
BIRD_COLOR = (255, 255, 0)
PIPE_COLOR = (0, 128, 0)
BACKGROUND_COLOR = (135, 206, 235)
GRAVITY = 0.5
FLAP_STRENGTH = 5
BLUR_RADIUS = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity_y = 0
        self.acceleration_y = 0.2
        self.friction = 0.99
        self.radius = BIRD_SIZE // 2

    def flap(self):
        self.velocity_y = -FLAP_STRENGTH

    def update(self):
        self.velocity_y += self.acceleration_y
        self.velocity_y *= self.friction
        self.y += self.velocity_y

    def draw(self):
        pygame.draw.circle(screen, BIRD_COLOR, (self.x, int(self.y)), self.radius)

    def get_pos(self):
        return np.array([self.x, self.y])

    def is_collision(self, pipe):
        bird_pos = self.get_pos()
        bird_radius = self.radius
        top_pipe_rect, bottom_pipe_rect = pipe.get_rects()

        if circle_rect_collision(bird_pos, bird_radius, top_pipe_rect):
            return True
        if circle_rect_collision(bird_pos, bird_radius, bottom_pipe_rect):
            return True
        return False

class Pipe:
    def __init__(self, x, gap_y, move_up_down):
        self.x = x
        self.gap_y = gap_y
        self.pipe_width = PIPE_WIDTH
        self.pipe_gap = PIPE_GAP
        self.move_up_down = move_up_down
        self.y_change = random.choice([-1, 1]) * 2 if move_up_down else 0
        self.max_height = SCREEN_HEIGHT - PIPE_GAP - 100
        self.min_height = 100

        if self.move_up_down:
            min_gap = 3 * BIRD_SIZE
            max_gap = self.max_height - min_gap
            self.pipe_gap = random.randint(min_gap, max_gap)

    def move(self):
        if self.move_up_down:
            self.gap_y += self.y_change
            if self.gap_y < self.min_height or self.gap_y > self.max_height:
                self.y_change *= -1
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

class Background:
    def __init__(self):
        self.image = pygame.image.load("background.png").convert()
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, self.rect)

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

def circle_rect_collision(circle_pos, circle_radius, rect):
    closest_x = max(rect.left, min(circle_pos[0], rect.right))
    closest_y = max(rect.top, min(circle_pos[1], rect.bottom))
    distance_squared = (circle_pos[0] - closest_x) ** 2 + (circle_pos[1] - closest_y) ** 2
    return distance_squared < circle_radius ** 2

def apply_blur_effect(surface, radius):
    rect = surface.get_rect()
    sub = surface.subsurface(rect)
    sub = pygame.transform.smoothscale(sub, (rect.width // 10, rect.height // 10))
    sub = pygame.transform.smoothscale(sub, (rect.width, rect.height))
    sub.set_alpha(150)
    surface.blit(sub, rect)

def main():
    mode_selected = False
    easy_mode = False
    hard_mode = False

    bird = Bird(100, SCREEN_HEIGHT // 2)
    background = Background()
    pipes = []
    clock = pygame.time.Clock()
    frame_count = 0
    game_over = False
    game_started = False

    while not mode_selected:
        screen.fill(BACKGROUND_COLOR)
        background.draw()

        easy_button = Button(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2, 200, 50, (0, 0, 255), "Easy Mode")
        hard_button = Button(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2, 200, 50, (0, 0, 255), "Hard Mode")

        easy_button.draw()
        hard_button.draw()

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if easy_button.is_clicked(mouse_pos):
                    easy_mode = True
                    mode_selected = True
                elif hard_button.is_clicked(mouse_pos):
                    hard_mode = True
                    mode_selected = True

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

        if game_started:
            bird.update()

            if bird.y + bird.radius > SCREEN_HEIGHT:
                game_over = True

            frame_count += 1
            if frame_count % 100 == 0:
                if easy_mode:
                    gap_y = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
                    new_pipe = Pipe(SCREEN_WIDTH, gap_y, False)
                elif hard_mode:
                    gap_y = SCREEN_HEIGHT // 2
                    new_pipe = Pipe(SCREEN_WIDTH, gap_y, True)
                pipes.append(new_pipe)

            for pipe in pipes:
                pipe.move()

            pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

            if any(bird.is_collision(pipe) for pipe in pipes):
                game_over = True

        screen.fill(BACKGROUND_COLOR)
        background.draw()
        bird.draw()
 
        for pipe in pipes:
            pipe.draw()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
 