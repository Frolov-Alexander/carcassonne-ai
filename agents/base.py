from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action


class Agent(ABC):
    """
    Base class for all Carcassonne agents.

    Each agent controls exactly one player index in the game.
    """

    def __init__(self, index: int, agent_type: str):
        self.index = index
        self.type = agent_type

    def choice(self, game: CarcassonneGame) -> Optional[Action]:
        """
        Called by the game loop to get this agent's next action.
        """
        return self.get_action(game)

    @abstractmethod
    def get_action(self, game: CarcassonneGame) -> Optional[Action]:
        """
        Implement this in subclasses.

        Should return:
          - an Action object, or
          - None to indicate 'pass' / no move.
        """
        raise NotImplementedError


class PlayerAgent(Agent):
    """
    Very simple human/terminal agent.

    For now this just prints the list of possible actions and lets the
    user choose by index. This is mainly for debugging / demo purposes.
    """

    def __init__(self, index: int):
        super().__init__(index, agent_type="Human")

    def get_action(self, game: CarcassonneGame) -> Optional[Action]:
        actions = game.get_possible_actions()
        if not actions:
            print(f"Agent({self.type}) {self.index}: pass (no actions)")
            return None

        print(f"\nAgent({self.type}) {self.index}, possible actions:")
        for i, act in enumerate(actions):
            print(f"  [{i}] {act}")

        while True:
            raw = input("Choose action index (or 'p' to pass): ").strip()
            if raw.lower() in {"p", "pass"}:
                print(f"Agent({self.type}) {self.index}: pass")
                return None

            if raw.isdigit():
                idx = int(raw)
                if 0 <= idx < len(actions):
                    chosen = actions[idx]
                    print(f"Agent({self.type}) {self.index}: {chosen}")
                    return chosen

            print("Invalid input, try again.")
