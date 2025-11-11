"""
Author: Ari Majumdar
Updated: 11/11/25
Version1

Based on wingedsheep's Carcassonne game implementation, Pacman project implementations, 
and [MCTS paper](https://arxiv.org/pdf/2009.12974) (Ameneyro et. al.)
We define a player agent and player state.


"""

import random

class Agent:
    """
    Agent must define a getAction method
    """
    def __init__(self,index=0):
        self.index = index

    def choice(self,valid_actions):
        action = random.choice(valid_actions)
        print(f"Agent_{self.index}: {action}")
        return action


    def getAction(self,state):
        raise NotImplementedError()
    
class GameAgent(Agent):
    def __init__(self, index):
        super().__init__(index)
    def getAction(self, state):
        pass

class PlayerAgent(Agent):
    def __init__(self, index):
        super().__init__(index)
    
    def getAction(self, state):
        pass