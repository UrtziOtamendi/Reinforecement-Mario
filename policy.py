import numpy as np
import random 
class Policy:

    '''''
        Actions
        
        Six possible actions:
                        
            - Up
            - Left
            - Down
            - Right
            - A
            - B
    
        Example:

            [0,0,0,0,0,0] -> Not moving
            [0,0,0,1,0,0] -> Moving right
            [0,0,0,1,0,1] -> Moving right + B
    '''''

    def __init__(self,max,reduction):
        self.actions=6
        self.iteration=0
        self.max_iteration=max
        self.reduction=reduction

    def epsilon(self):
        if self.iteration > self.max_iteration:
            return 0.1
        else:
            return 1 - (self.reduction*self.iteration)


    def random(self):
        return np.random.randint(2,size=self.actions)

    def action(self):
        self.iteration+=1
        if(self.iteration % 100 == 0):
            print("----> Iteration nº {}".format(self.iteration))
        epsilon=self.epsilon()
        if random.uniform(0,1)<epsilon:
            return self.random()
        else:
            return self.random()