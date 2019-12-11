class StateController:

    def __init__(self,state_frames):
        self.frames=state_frames
        self.states_buffer=[State([None],None,None,None,None, None) for i in range(self.frames)]
        self.last_state=None

    def change_state(self,observation,action,reward,is_done,player_status):
        #Update last states next observations and save 
        
        self.last_state=self.states_buffer[0]

        for i in range(1,len(self.states_buffer)):
            #Update states next observations and move forward
            self.states_buffer[i].add_observation(observation)
            self.states_buffer[i-1]=self.states_buffer[i]
            
        #Create new state and insert in the last position
        # Last states (LS) next observations (NO) are newest states (NS) starting observations (SO)
        #  [SO2,SO1] -> LS.action -> [SO1,NO1] -> S.action -> [NO1,NO2] -> NS.action
        #  [SO2,SO1] -> LS.action -> [NO1,NO2]
        new_state=State(self.last_state.next,reward,action,is_done,observation,player_status)
        self.states_buffer[len(self.states_buffer)-1]=new_state
        return self.last_state
        
    def current_state(self):
        return self.states_buffer[len(self.states_buffer)-1]

    def __str__(self):
        string = ""
        for state in self.states_buffer:
            print(state)

        return string

class State:

    

    def __init__(self,start,reward,action,is_done,observation,player_status):
        # If start is None that means there have not passed yet enough states 
        # to have recorded the needed amount of frames on start observations
        if start[0] is None:
            self.is_valid=False
        else:
            self.is_valid=True
        self.start=start
        self.reward=reward
        self.action=action
        self.is_done=is_done
        self.player_status=player_status
        self.next=[observation]

    def add_observation(self,observation):
        self.next.append(observation)
        

    def __str__(self):
        header="--- State RESUME --- \n"
        start="- Start : "+ str(self.start) +"    \n"
        reward="- Reward : "+ str(self.reward) +"    \n"
        action="- Action : "+ str(self.action) +"    \n"
        is_done="- Is_done : "+ str(self.is_done) +"    \n"
        player_status=" - Player Status : "+str(self.player_status)+" \n"
        next_str= "- Next : "+ str(self.next) +"    \n"
        is_valid= "- Is-valid : "+str(self.is_valid)+"\n"
        return header+start+reward+action+is_done+player_status+next_str+is_valid  





    