import numpy as np
from keras.utils.np_utils import to_categorical

from constants import *

class Agent:
    def get_action(self, state, epoch, main_model):
        epsilon = 0.2

        if epsilon < np.random.uniform(0, 1):
            action = main_model.model.predict(state.reshape(1, S_STATE))[0].argmax()
        else:
            action = np.random.choice([0] * 30 + [1])

        return to_categorical(action, S_ACTION)
