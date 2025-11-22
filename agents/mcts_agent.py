# agents/mcts_agent.py

from __future__ import annotations

import random
from typing import Optional

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action

from .base import Agent
from MCTS.algorithm import MCTS  # your existing class


class MCTSAgent(Agent):
    """
    Agent that uses MCTS to choose its move.

    Right now this is a light wrapper. Once your MCTS implementation
    can work from an arbitrary CarcassonneGame state, you can plug it in
    here. Until then, we fall back to a random choice so the code runs.
    """

    def __init__(self, index: int, iterations: int = 100):
        super().__init__(index)
        self.type = "MCTS"
        self.iterations = iterations

    def getAction(self, game: CarcassonneGame) -> Optional[Action]:
        valid_actions = game.get_possible_actions()
        if not valid_actions:
            return None

        # TODO: wire this to your MCTS class.
        # Example sketch (you'll adapt algorithm.MCTS accordingly):
        #
        # mcts = MCTS(root_state=game.state, player_index=self.index)
        # for _ in range(self.iterations):
        #     mcts.one_iteration()
        # return mcts.best_action()
        #
        # For now, just behave randomly so nothing crashes:
        return random.choice(valid_actions)
