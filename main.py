from environment import Environment
from policy import Policy


## Init environment
environment = Environment()

## Init policy 
policy = Policy()


observation = environment.reset()
done = False
t = 0
while not done:
    action = policy.random()  # choose random action
    observation, reward, done, info = environment.step(action)  # feedback from environment
    t += 1
    if not t % 100:
        print(t, info)
environment.close()