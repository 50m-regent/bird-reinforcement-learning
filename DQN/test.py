import pygame
from numpy import array

from flappy_bird import FlappyBird

def main():
    clock = pygame.time.Clock()

    game = FlappyBird(1)

    running = True
    while running:
        clock.tick(60)

        actions = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                actions.append(array([0, 1]))
            
        if len(actions) == 0:
            actions.append(array([1, 0]))

        game.step(actions)

        if not len(game.birds):
            running = False
            break

        game.draw()

    print('\tScore: {}'.format(game.score))
    
    pygame.quit()

if __name__ == '__main__':
    main()