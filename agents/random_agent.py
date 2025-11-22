from __future__ import annotations

import random
from typing import Optional

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action

from .base import Agent


class RandAgent(Agent):
    """
    Baseline random agent: picks a random valid action.
    """

    def __init__(self, index: int):
        super().__init__(index, agent_type="Rand")

    def get_action(self, game: CarcassonneGame) -> Optional[Action]:
        actions = game.get_possible_actions()
        if not actions:
            print(f"Agent({self.type}) {self.index}: pass (no actions)")
            return None

        chosen = random.choice(actions)
        print(f"Agent({self.type}) {self.index}: {chosen}")
        return chosen
