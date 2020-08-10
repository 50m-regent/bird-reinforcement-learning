import neat
import pygame

from flappy_bird import FlappyBird

CFG_PATH = 'neat_config.txt'
NUM_BIRD = 50

env = FlappyBird(NUM_BIRD)

def gen(genomes, config):
    clock = pygame.time.Clock()
    env.reset()

    nets = []
    ge   = []
    for _, g in genomes:
        nets.append(neat.nn.FeedForwardNetwork.create(g, config))
        g.fitness = 0
        ge.append(g)

    while len(env.birds) > 0:
        clock.tick(60)
        for pipe in env.pipes:
            if pipe.move():
                env.score += 1

                for g in ge:
                    g.fitness += 3

        pipe_idx = 0
        while env.birds[0].rect.x > env.pipes[pipe_idx].top_rect.left:
            pipe_idx += 1

        for i, bird in enumerate(env.birds):
            try:
                output = nets[i].activate((
                    bird.rect.y,
                    env.pipes[pipe_idx].top_rect.bottom - bird.rect.y,
                    env.pipes[pipe_idx].top_rect.left - bird.rect.x))
                if output[0] > 0.5:
                    bird.jump()

                bird.move()
                ge[i].fitness += 0.1

                if env.check_collide(bird):
                    ge[i].fitness -= 1

                    env.birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)
            except:
                pass

        env.draw()

def train():
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        CFG_PATH)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())

    winner = p.run(gen, NUM_BIRD)

    pygame.quit()

if __name__ == '__main__':
    train()