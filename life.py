class Life:
    def __init__(self):
        self.score=0
        self.total_reward=0
        self.player_status=0
        
    def update(self,info):
        self.player_status=info["status"]
        self.score=info["score"]

    def __str__(self):
        header="--- LIFE RESUME --- \n"
        score="- Score : "+ str(self.score) +"    \n"
        total_reward="- Total Reward : "+ str(self.total_reward) +"    \n"
        return header+score+total_reward  

