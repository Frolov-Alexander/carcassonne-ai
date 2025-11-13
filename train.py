from MCTS.algorithm import MCTS

if __name__ == '__main__':
    mcts = MCTS()
    for _ in range(10):
        mcts.one_iteration()