from .node import MCTSNode

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet


class MCTS:
    def __init__(self):
        self.root = None
        self.c = 9999

        new_game = CarcassonneGame(
            players=2,
            tile_sets=[TileSet.BASE],
            supplementary_rules=[],
        )

        self.root = MCTSNode(state=new_game.state, exploration_rate=0.3)

    def run(self):
        pass

    def one_iteration(self):
        node_gen = self.root.select_expand()
        terminal_state = node_gen.rollout()
        node_gen.update(
            win=terminal_state.scores[0] > terminal_state.scores[1],
            result=terminal_state.scores[0] - terminal_state.scores[1]
        )

        self.visualize()

    def visualize(self):
        # BFS print
        print("===========================================")
        print("Tree Visualization:")
        queue = [(self.root, 0)]
        while queue:
            entry = queue.pop(0)
            current_node = entry[0]
            level = entry[1]
            print(f"{' '*level}Node: Visits={current_node.visits}, Wins={current_node.wins}, Children={current_node.children}")
            for child in current_node.children.values():
                queue.append((child, level + 1))
        print("===========================================")

