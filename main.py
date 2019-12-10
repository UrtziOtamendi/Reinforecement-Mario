from environment import Environment
from policy import Policy
from game import Game
from life import Life
## Init environment
environment = Environment()

## Init policy 
policy = Policy()

## Init Game controller
game_controller= Game()


## Is dead?
is_dead = game_controller.is_dead()


## Main loop
while not is_dead:
    ## Reset environment
    observation = environment.reset()

    ## New Life
    life=Life()
    ## Is done?
    is_done = False

    while not is_done:
        # Use policy
        action = policy.random()  # choose random action
        
        # Make an action
        observation, reward, is_done, info = environment.step(action)  # feedback from environment

        # Update life
        life.update(info)
    
    
    # Prin life resume
    print(life)
    #Update game controller
    game_controller.update(info,is_done)
    is_dead = game_controller.is_dead()

print(game_controller)
environment.close()