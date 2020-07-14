import random
import numpy as np
class StateBuffer:

    def __init__(self,size):
        self.data = [None] * (size + 1)
        self.start = 0
        self.end = 0
    
    def append(self,state):
        if state.is_valid:
            self.data[self.end]=state
            self.end=(self.end+1) % len(self.data)
            if self.end == self.start:
                ##Save states
                

                self.start = (self.start + 1) % len(self.data)

    def batch(self,size):
        batch=[]
        state=[]
        next_state=[]
        action=[]
        reward=[]
        done=[]
        if(self.end<size):
            return batch
        else:
            index=random.sample(range(0,self.end), size)
            for i in index:
                state.append(self.data[i].start)
                next_state.append(self.data[i].next)
                action.append(self.data[i].action)
                reward.append(self.data[i].reward)
                done.append(self.data[i].is_done)
            batch=[state,next_state,action,np.array(reward),np.array(done)]
            return batch
    
    def __getitem__(self, idx):
        return self.data[(self.start + idx) % len(self.data)]
    
    def __len__(self):
        if self.end < self.start:
            return self.end + len(self.data) - self.start
        else:
            return self.end - self.start
        
    def __iter__(self):
        for i in range(len(self)):
            yield self[i]