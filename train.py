"""
import training function
"""

from agents.training.train_MCTS import train as mcts_train
from agents.training.train_Q import train as q_train

AGENT_DIR = 'agents/'
PARAM_DIR = 'agents/params/'

train = q_train

if __name__ == '__main__':
    train()