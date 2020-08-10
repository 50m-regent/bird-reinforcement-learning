import pygame

from flappy_bird import FlappyBird
from model import Model
from memory import Memory
from agent import Agent

def evaluate(env, agent):
    env.reset()
    state, _, finished = env.random_step()
    while not finished:
        action = agent.get_action(state, N_EPOCHS, main_model)
        next_state, _, finished = env.step(action.argmax(), verbose=True)
        state = next_state

def main():
    clock = pygame.time.Clock()

    N_EPOCHS = 1000
    GAMMA    = 0.99
    N_BIRD   = 64
    S_BATCH  = 256

    env = FlappyBird(N_BIRD)

    main_model   = Model()
    target_model = Model()

    memory = Memory()
    agent  = Agent()

    for epoch in range(1, N_EPOCHS + 1):
        print('Epoch: {}'.format(epoch))

        env.reset()
        states, rewards, finished = env.random_step() 
        target_model.model.set_weights(main_model.model.get_weights())

        running = True
        while running:
            clock.tick(60)

            actions = []
            for state in states:
                actions.append(agent.get_action(state, epoch, main_model))

            next_states, rewards, finished = env.step(actions)
            for state, reward, action, next_state in zip(states, rewards, actions, next_states):
                memory.add((state, action, reward, next_state))

            states = next_states

            if len(memory.buffer) % S_BATCH == 0:
                main_model.replay(memory, env.n_bird, GAMMA, target_model)

            target_model.model.set_weights(main_model.model.get_weights())

            if not len(env.birds):
                running = False
                break

            env.draw()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

        print('\tScore: {}'.format(env.score))
    
    pygame.quit()

    env = FlappyBird()
    # evaluate(env, agent)

if __name__ == '__main__':
    main()