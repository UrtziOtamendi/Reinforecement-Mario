from environment import Environment
from policy import Policy
from game import Game
from life import Life
from stateController import StateController
from stateBuffer import StateBuffer

## Init environment
environment = Environment()

## Init policy 
max_epsilon_it=1000000
epsilon_reduction=9e-7
policy = Policy(max_epsilon_it,epsilon_reduction)

## Init Game controller
gameController= Game()

##Init state controller
state_frames=4
stateController= StateController(state_frames)

##Init State buffer
buffer_size=10000
stateBuffer= StateBuffer(buffer_size)


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
        action = policy.action()  # choose random action
        
        # Make an action
        observation, reward, is_done, info = environment.step(action)  # feedback from environment
        
        # Update life
        life.update(info)
    
        #update state
        last_state=stateController.change_state(observation,action,reward,is_done,life.player_status)
        
        #Save state
        stateBuffer.append(last_state)
        
        
    
    # Prin life resume
    print(life)
    #Update game controller
    gameController.update(info,is_done)
    is_dead = gameController.is_dead()

print(gameController)
environment.close()