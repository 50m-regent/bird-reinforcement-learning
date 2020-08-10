import pygame
import random
import sys
import math
from numpy import array

WIN_WIDTH  = 600
WIN_HEIGHT = 800

COLORS = {
    'sky':    (135, 206, 250),
    'bird':   (255, 255, 0),
    'pipe':   (50,  205, 50),
    'ground': (160, 82,  45)
}

BIRD_SIZE = 50

PIPE_VEL = 4
PIPE_GAP = 200
PIPE_WIDTH  = 100
PIPE_MARGIN = 100

GROUND_HEIGHT = 100

class Bird:
    def __init__(self, x=200, y=350):
        self.y = y
        self.vel = 0
        self.rect = pygame.Rect(x, self.y, BIRD_SIZE, BIRD_SIZE)

    def jump(self):
        self.vel = -6

    def move(self):
        self.vel += 0.4

        self.y += self.vel

        self.rect.top = self.y

    def get_state(self):
        return [self.y, self.vel]

    def draw(self, win):
        pygame.draw.rect(win, COLORS['bird'], self.rect)

class Pipe:
    def __init__(self, x=700):
        self.top    = random.randrange(PIPE_MARGIN, WIN_HEIGHT - PIPE_GAP - PIPE_MARGIN - GROUND_HEIGHT)
        self.bottom = self.top + PIPE_GAP

        self.top_rect    = pygame.Rect(x, 0, PIPE_WIDTH, self.top)
        self.bottom_rect = pygame.Rect(x, self.bottom, PIPE_WIDTH, WIN_HEIGHT - self.bottom)

    def move(self):
        self.top_rect    = self.top_rect.move(-PIPE_VEL, 0)
        self.bottom_rect = self.bottom_rect.move(-PIPE_VEL, 0)

        if self.top_rect.left < -PIPE_WIDTH:
            self.__init__()

        return self.top_rect.left == 200

    def draw(self, win):
        pygame.draw.rect(win, COLORS['pipe'], self.top_rect)
        pygame.draw.rect(win, COLORS['pipe'], self.bottom_rect)
        
class Ground:
    def __init__(self):
        self.rect = pygame.Rect(0, WIN_HEIGHT - GROUND_HEIGHT, WIN_WIDTH, GROUND_HEIGHT)

    def draw(self, win):
        pygame.draw.rect(win, COLORS['ground'], self.rect)

class FlappyBird:
    def __init__(self, n_bird=1):
        pygame.init()
        self.win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption('Flappy Bird')

        self.n_bird = n_bird
        self.birds  = [Bird() for _ in range(self.n_bird)]
        self.pipes  = [Pipe(800), Pipe(1200)]
        self.ground = Ground()

        self.score = 0
        
    def reset(self):
        self.__init__(self.n_bird)

    def draw(self):
        self.win.fill(COLORS['sky'])

        for bird in self.birds:
            bird.draw(self.win)

        for pipe in self.pipes:
            pipe.draw(self.win)

        self.ground.draw(self.win)

        pygame.display.update()

    def check_collide(self, bird):
        if bird.y <= -BIRD_SIZE:
            return True

        for pipe in self.pipes:
            if pipe.top_rect.colliderect(bird.rect) or pipe.bottom_rect.colliderect(bird.rect):
                return True

        if self.ground.rect.colliderect(bird.rect):
            return True

        return False

    def step(self, actions):
        passed = False

        for pipe in self.pipes:
            if pipe.move():
                self.score += 1
                passed = True

        next_birds = []
        states     = []
        rewards    = []

        for action, bird in zip(actions, self.birds):
            if action.argmax():
                bird.jump()

            last_y = bird.y

            bird.move()

            pipe_idx = 0
            while bird.rect.x > self.pipes[pipe_idx].top_rect.left:
                pipe_idx += 1

            rewards.append(
                1 if abs(self.pipes[pipe_idx].top_rect.bottom + PIPE_GAP / 2 - last_y) < abs(self.pipes[pipe_idx].top_rect.bottom + PIPE_GAP / 2 - bird.y) else 0
            )

            pipe_state = [
                self.pipes[pipe_idx].top_rect.bottom - bird.y,
                self.pipes[pipe_idx].top_rect.left - 200
            ]

            states.append(bird.get_state() + pipe_state)

            finished = self.check_collide(bird)
            if not finished:
                next_birds.append(bird)

        self.birds = next_birds

        return array(states), array(rewards), finished

    def random_step(self):
        for pipe in self.pipes:
            pipe.move()

        state = []
        for bird in self.birds:
            pipe_state = [
                self.pipes[0].top_rect.bottom - bird.y,
                self.pipes[0].top_rect.left - 200
            ]

            state.append(bird.get_state() + pipe_state)

        return array(state), array([0 for _ in range(self.n_bird)]), False
