import gym_super_mario_bros
from nes_py.wrappers import JoypadSpace
from gym_super_mario_bros.actions import COMPLEX_MOVEMENT 

class Environment:

    def __init__(self):
        
        env=gym_super_mario_bros.make('SuperMarioBros-1-1-v0')
        self.env=JoypadSpace(env,COMPLEX_MOVEMENT)
        ##self.env.no_render = False
    def reset(self):
        observation =self.env.reset()
        return observation

    def close(self):
        self.env.close()

    def step(self,action):
        observation, reward, done, info = self.env.step(action)
        return observation, reward, done, info

    def actionSpace(self):
        return self.env.action_space

   
        