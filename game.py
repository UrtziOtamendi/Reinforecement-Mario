class Game:

    def __init__(self):
        self.lifes=3
        self.total_reward=0
        self.scores=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.locked_levels =[False, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True]
    
    def update(self,info,is_done):
        
        if is_done:
            self.lifes -=1
        
        self.total_reward=info['total_reward']
        self.scores=info['scores']
        self.locked_levels=info['locked_levels']
        


    def is_dead(self):
        if self.lifes==0:
            return True

    def __str__(self):
        header="--- GAME RESUME --- \n"
        lifes="- Lifes : "+ str(self.lifes) +"    \n"
        total_reward="- Total Reward : "+ str(self.total_reward) +"    \n"
        scores="- Scores : "+str(self.scores)[1:-1]+" \n"
        locked_levels="- Locked levels : "+str(self.locked_levels)[1:-1]+"\n"
        return header+lifes+total_reward+scores+locked_levels  
