import numpy as np
import random 


class Policy:


    def __init__(self,max,reduction,action_space):
        self.action_space=action_space
        self.iteration=0
        self.max_iteration=max
        self.reduction=reduction

    def epsilon(self):
        if self.iteration > self.max_iteration:
            return 0.1
        else:
            return 1 - (self.reduction*self.iteration)


    def random(self):
        return self.action_space.sample()

    def action(self):
        self.iteration+=1
        epsilon=self.epsilon()
        if random.uniform(0,1)<epsilon:
            return self.random()
        else:
            return None