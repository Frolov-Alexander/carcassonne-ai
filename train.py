# from MCTS.algorithm import MCTS
# from agents.training.train_MCTS import train
from agents.training.train_Q import train

AGENT_DIR = 'agents/'
PARAM_DIR = 'agents/params/'

# AGENT_TO_TRAIN = MCTS()

if __name__ == '__main__':
    train()