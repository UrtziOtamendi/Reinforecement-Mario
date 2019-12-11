from environment import Environment
from policy import Policy
from game import Game
from life import Life
from stateController import StateController
## Init environment
environment = Environment()

## Init policy 
policy = Policy()

## Init Game controller
gameController= Game()

##Init state controller
state_frames=4
stateController= StateController(state_frames)

## Is dead?
is_dead = gameController.is_dead()


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

        #update state
        stateController.change_state(observation,action,reward,is_done)
        
        

        # Update life
        life.update(info)
    
    
    # Prin life resume
    print(life)
    #Update game controller
    gameController.update(info,is_done)
    is_dead = gameController.is_dead()

print(gameController)
environment.close()