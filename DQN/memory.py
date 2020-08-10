from collections import deque
import numpy as np

class Memory:
    def __init__(self):
        self.buffer = deque()

    def add(self, exp):
        self.buffer.append(exp)

    def sample(self, batch_size):
        indice = np.random.choice(np.arange(len(self.buffer)), size=batch_size, replace=False)
        ret = [self.buffer[i] for i in indice]
        return ret
