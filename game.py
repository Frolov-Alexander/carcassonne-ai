import random
from typing import Optional

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.tile_sets.tile_sets import TileSet
from wingedsheep.carcassonne.tile_sets.supplementary_rules import SupplementaryRule

from agents import Agent, RandAgent, PlayerAgent, QLearnAgent


def main() -> None:
    # --- configure game (you can later hook this up to a UI/menu) ---
    game = CarcassonneGame(
        players=2,
        tile_sets=[TileSet.BASE],
        supplementary_rules=[],  # e.g. [SupplementaryRule.ABBOTS, SupplementaryRule.FARMERS]
    )

    # Example setups:
    # players = [RandAgent(i) for i in range(game.players)]
    # players = [PlayerAgent(0), RandAgent(1)]

    q_agent = QLearnAgent(
        0,
        epsilon=0.0,           # exploit only
        load_path="q_table.pkl"
    )
    
    # Q-learning vs random baseline:
    players: list[Agent] = [
        q_agent,  # or load_path="q_table.pkl"
        RandAgent(1),
    ]

    # --- main game loop ---
    while not game.is_finished():
        player_id: int = game.get_current_player()
        agent: Agent = players[player_id]

        action: Optional[Action] = agent.choice(game)
        if action is not None:
            game.step(player_id, action)

        game.render()

    print("Game finished. Final scores:", game.state.scores)


if __name__ == "__main__":
    main()
