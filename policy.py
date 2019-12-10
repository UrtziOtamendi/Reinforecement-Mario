import numpy as np
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

    def __init__(self):
        self.actions=6


    def random(self):
        return np.random.randint(2,size=self.actions)

    
