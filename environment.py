import gym


class Environment:

    def __init__(self):
        self.env=gym.make('SuperMarioBros-1-1-v0')

    def reset(self):
        observation =self.env.reset()
        return observation

    def step(self,action):
        observation, reward, done, info = self.env.step(action)
        return observation, reward, done, info


   
        