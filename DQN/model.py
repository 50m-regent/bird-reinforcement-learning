from keras.models import Sequential
from keras.layers import Dense, Reshape
from tensorflow.keras.optimizers import Adam
import numpy as np

from constants import *

class Model:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(S_HIDDEN, activation='relu', input_dim=S_STATE))
        self.model.add(Dense(S_ACTION, activation='softmax'))
        self.optimizer = Adam(lr=LR)
        self.model.compile(loss='mse', optimizer=self.optimizer)
        self.model.summary()

    def replay(self, memory, batch_size, gamma, target_model):
        inputs     = np.zeros((batch_size, S_STATE))
        outputs    = np.zeros((batch_size, S_ACTION))
        mini_batch = memory.sample(batch_size)

        for i, (state, action, reward, next_state) in enumerate(mini_batch):
            inputs[i:i + 1] = state
            target          = reward

            if not (next_state == np.zeros(state.shape)).all():
                q = self.model.predict(next_state.reshape(1, S_STATE))[0].argmax()
                next_action = np.argmax(q) # 最もQ値が高い行動を次の行動として選択
                target = reward + gamma * target_model.model.predict(
                    next_state.reshape(1, S_STATE)
                )[0][next_action]

            outputs[i] = self.model.predict(state.reshape(1, S_STATE))
            outputs[i][action.argmax()] = target

        self.model.fit(inputs, outputs, epochs=1, verbose=0)