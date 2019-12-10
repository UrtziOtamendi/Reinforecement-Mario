import gym


class Environment:

    def __init__(self):
        self.env=gym.make('SuperMarioBros-1-1-Tiles-v0')
        ##self.env.no_render = False
    def reset(self):
        observation =self.env.reset()
        return observation

    def close(self):
        self.env.close()

    def step(self,action):
        observation, reward, done, info = self.env.step(action)
        return observation, reward, done, info


   
        