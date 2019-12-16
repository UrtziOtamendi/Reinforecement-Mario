from environment import Environment
from policy import Policy
from game import Game
from life import Life
from stateController import StateController
from stateBuffer import StateBuffer
from DQN import DQNAgent
from logger import Logger
import time
BATCH_SIZE = 32



## Init environment
environment = Environment()

## Init policy 
max_epsilon_it=1000000
epsilon_reduction=9e-7
policy = Policy(max_epsilon_it,epsilon_reduction,environment.actionSpace())

## Init Game controller
gameController= Game()

##Init state controller
state_frames=4

stateController= StateController(state_frames)

##Init State buffer
buffer_size=10000
stateBuffer= StateBuffer(buffer_size)

##Init DQN model
actions=policy.action_space.n
states=(84,84,state_frames)
DQNmodel= DQNAgent(states,actions, double_q=True)

#Init logger
logger=Logger("./logs")


# Timing
start = time.time()

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
        action = policy.action()  # choose action using policy 
        if action is None:
            #Check if current state is valid
            current_state=stateController.current_state()
            if current_state.is_valid:
                # In case current state is valid select action using DQN model
                action=DQNmodel.run(state=current_state)
            else:
                # In case current state is not valid select random action
                action= policy.random()

        # Make an action
        observation, reward, is_done, info = environment.step(action)  # feedback from environment
        
        # Update life
        life.update(info)

        #update state
        last_state=stateController.change_state(observation,action,reward,is_done,life.player_status)
        
        #Save state
        stateBuffer.append(last_state)

        #Learn Model
        training_batch=stateBuffer.batch(BATCH_SIZE)
        if training_batch!=[]:
            DQNmodel.learn(training_batch)
        
        if policy.iteration % 100 ==0:
            print(policy.iteration)
            print(time.time() - start)
            print(life)

    

    # Prin life resume
    print(life)

    #Logg
    logger.record(life.score)
    #Update game controller
    gameController.update(info,is_done)

    # Play with lives
    ##is_dead = gameController.is_dead()
    # Play infinite
    is_dead=False

print(gameController)

environment.close()

