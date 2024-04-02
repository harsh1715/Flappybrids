import pygame
import sys
import random
import numpy as np
from pygame.locals import *

pygame.init()

# Global Variables
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
WHITE = (255, 255, 255)
DGREEN = (1, 50, 32)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Game")

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


def display_text(surface, text, pos, font, color):
    collection = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    x,y = pos
    for lines in collection:
        for words in lines:
            word_surface = font.render(words, True, color)
            word_width , word_height = word_surface.get_size()
            if x + word_width >= SCREEN_WIDTH:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x,y))
            x += word_width + space
        x = pos[0]
        y += word_height


def introduction_screen():
    intro = """               Welcome to Flappy Birds! Here are Rules for our simple game:

1) Press the spacebar to flap the bird's wings and navigate through the pipes.

2) Your goal is to pass through as many pipes as possible without colliding with them.

3) Each successful pass through a pair of pipes earns you one point.

4) Be cautious! If the bird touches the ground or the pipes, the game is over.

5) Easy Mode features pipes with randomly spaced gaps, providing a simpler gameplay experience. 

6) If you choose hard mode, the pipes dynamically move up and down, altering the gaps between them, offering a more challenging gameplay.


                        Select the game difficulty mode in the next window

                                         Click SPACE to continue...
    """

    font = pygame.font.SysFont("COMICSANS", 19)
    screen.fill(WHITE)
    display_text(screen, intro, (20, 20), font, RED)
    pygame.display.update()
 
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return


def game_over_screen(points):
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.SysFont("COMICSANS", 19)

    # Displaying "Game Over" text
    game_over_text = font.render("Game Over", True, RED)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(game_over_text, game_over_rect)

    # Displaying points scored
    points_text = font.render("Points: " + str(points), True, WHITE)
    points_rect = points_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(points_text, points_rect)

    # Displaying "Play Again" button
    play_again_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50, 200, 50, (0, 255, 0), "Play Again")
    play_again_button.draw()

    pygame.display.flip()

    # Waiting for user input to play again or quit
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.is_clicked(mouse_pos):
                    return True 
        pygame.time.Clock().tick(30)


def start_menu():
    mode_selected = False
    easy_mode = False
    hard_mode = False

    while not mode_selected:
        screen.fill(BACKGROUND_COLOR)
        background = Background()
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

    return easy_mode, hard_mode


def main():
    introduction_screen() 
    while True:
        easy_mode, hard_mode = start_menu()
        points = 0
        bird = Bird(100, SCREEN_HEIGHT // 2)
        background = Background()
        pipes = []
        clock = pygame.time.Clock()
        frame_count = 0
        game_over = False
        game_started = False

        font = pygame.font.Font(None, 36)

        space_clicked = False

        space_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 100, 300, 50, (255, 0, 0), "Click SPACE to Start")

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
                            space_clicked = True

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

                for pipe in pipes:
                    if pipe.x + PIPE_WIDTH // 2 == bird.x:
                        points += 1

                if any(bird.is_collision(pipe) for pipe in pipes):
                    game_over = True

            screen.fill(BACKGROUND_COLOR)
            background.draw()
            bird.draw()

            for pipe in pipes:
                pipe.draw()

            if not space_clicked:
                space_button.draw()

            points_text = font.render("Points: " + str(points), True, (255, 255, 255))
            points_rect = points_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
            screen.blit(points_text, points_rect)

            pygame.display.flip()
            clock.tick(60)

        while game_over:
            play_again = game_over_screen(points)
            if play_again:
                break
            else:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()