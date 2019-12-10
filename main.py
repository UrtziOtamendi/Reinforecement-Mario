from environment import Environment
from policy import Policy
from game import Game

## Init environment
environment = Environment()

## Init policy 
policy = Policy()

## Init Game controller
game_controller= Game()

## Iteration counter
iterations=0

## Is dead?
is_dead = game_controller.is_dead()

## Is done?
is_done = False

## Reset environment
observation = environment.reset()

## Main loop
while not is_dead:

    # Use policy
    action = policy.random()  # choose random action
    
    # Make an action
    observation, reward, is_done, info = environment.step(action)  # feedback from environment
    
    #Update game controller
    game_controller.update(info,is_done)
    is_dead = game_controller.is_dead()
    is_done=False
    iterations += 1
    if not iterations % 100:
        print(iterations, info)

print(game_controller)
environment.close()