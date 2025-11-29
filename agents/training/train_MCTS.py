from MCTS.algorithm import MCTS


AGENT_ID = 1
QTABLE_FILEPATH = f'agents/params/mcts_nodes_{AGENT_ID}.pkl'
TRAINING_ITERATIONS = 5



def train(episodes, agent_filepath):
    mcts = MCTS()
    for _ in range(10):
        mcts.one_iteration()