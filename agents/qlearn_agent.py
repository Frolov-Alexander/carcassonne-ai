from __future__ import annotations

import pickle
import random
from typing import Optional, Dict, Tuple

from wingedsheep.carcassonne.carcassonne_game import CarcassonneGame
from wingedsheep.carcassonne.objects.actions.action import Action

from .base import Agent


StateKey = Tuple[str, int, int, str]  # (tile_name, score_bucket, meeples_left, phase)
ActionKey = str                       # repr(action)


class QLearnAgent(Agent):
    """
    Tabular Q-learning agent.

    - Keeps a Q-table: key = (state_key, action_key)
    - Uses epsilon-greedy policy over valid actions
    - Reward = change in this player's score since its last move
    """

    def __init__(
        self,
        index: int,
        alpha: float = 0.3,
        gamma: float = 0.9,
        epsilon: float = 0.2,
        load_path: str | None = None,
    ):
        super().__init__(index, agent_type="Qlearn")

        # Q[(state_key, action_key)] -> value
        self.q_table: Dict[Tuple[StateKey, ActionKey], float] = {}

        # hyperparameters
        self.alpha = alpha      # learning rate
        self.gamma = gamma      # discount factor
        self.epsilon = epsilon  # exploration rate

        # memory of previous transition (for Q update)
        self.last_state_key: Optional[StateKey] = None
        self.last_action_key: Optional[ActionKey] = None
        self.last_score: int = 0

        if load_path is not None:
            self.load_q_table(load_path)

    # ---------- episode-level helpers ----------

    def reset_episode(self) -> None:
        """
        Reset per-episode memory, but keep the learned Q-table.
        Call this at the start of each training game.
        """
        self.last_state_key = None
        self.last_action_key = None
        self.last_score = 0

    # ---------- helpers to encode state / action ----------

    def _encode_state(self, game: CarcassonneGame) -> StateKey:
        """Turn the big game state into a compact, hashable key."""
        state = game.state

        # 1) tile in hand
        next_tile = getattr(state, "next_tile", None)
        if next_tile is None:
            tile_name = "NO_TILE"
        else:
            tile_name = getattr(next_tile, "name", None)
            if tile_name is None:
                tile_name = getattr(next_tile, "id", None) or getattr(
                    next_tile, "tile_id", None
                )
            if tile_name is None:
                tile_name = type(next_tile).__name__

        # 2) score difference bucketed
        my_score = state.scores[self.index]
        opp_index = 1 - self.index  # assumes 2-player for now
        opp_score = state.scores[opp_index]
        diff = my_score - opp_score
        if diff < -5:
            score_bucket = -1
        elif diff > 5:
            score_bucket = 1
        else:
            score_bucket = 0

        # 3) how many meeples left
        meeples_left = state.meeples[self.index]

        # 4) game phase (tiles vs meeples etc.)
        phase_obj = getattr(state, "phase", None)
        if phase_obj is None:
            phase_name = "UNKNOWN_PHASE"
        else:
            phase_name = getattr(phase_obj, "name", type(phase_obj).__name__)

        return (tile_name, score_bucket, meeples_left, phase_name)

    def _encode_action(self, action: Action) -> ActionKey:
        # repr() is stable and already used in printing
        return repr(action)

    # ---------- main RL logic ----------

    def get_action(self, game: CarcassonneGame) -> Optional[Action]:
        """
        Called once per turn.

        1) Use current game.state to update Q for the *previous*
           (state, action) pair based on score change.
        2) Choose next action with epsilon-greedy policy.
        3) Store (state, action, score) to update on the next turn.
        """
        valid_actions = game.get_possible_actions()
        if not valid_actions:
            # still update Q for the previous move if needed
            current_state_key = self._encode_state(game)
            current_score = game.state.scores[self.index]
            self._update_q(current_state_key, current_score, [])
            print(f"Agent({self.type}) {self.index}: pass (no actions)")
            return None

        current_state_key = self._encode_state(game)
        current_score = game.state.scores[self.index]

        # update Q for previous state/action if we have one
        self._update_q(current_state_key, current_score, valid_actions)

        # epsilon-greedy selection in current state
        if random.random() < self.epsilon:
            chosen_action = random.choice(valid_actions)
        else:
            best_q = float("-inf")
            chosen_action = None
            for act in valid_actions:
                a_key = self._encode_action(act)
                q_val = self.q_table.get((current_state_key, a_key), 0.0)
                if q_val > best_q:
                    best_q = q_val
                    chosen_action = act
            if chosen_action is None:
                chosen_action = random.choice(valid_actions)

        # remember for next update
        self.last_state_key = current_state_key
        self.last_action_key = self._encode_action(chosen_action)
        self.last_score = current_score

        print(f"Agent({self.type}) {self.index}: {chosen_action}")
        return chosen_action

    def _update_q(
        self,
        current_state_key: StateKey,
        current_score: int,
        valid_actions: list[Action],
    ) -> None:
        """
        Internal helper: perform the Q-learning update for the previous
        (state, action) -> new_state transition.
        """
        if self.last_state_key is None or self.last_action_key is None:
            return

        # reward = change in my score since my last move
        reward = current_score - self.last_score

        # max future Q (bootstrap)
        max_future_q = 0.0
        for act in valid_actions:
            a_key = self._encode_action(act)
            max_future_q = max(
                max_future_q,
                self.q_table.get((current_state_key, a_key), 0.0),
            )

        old_q = self.q_table.get((self.last_state_key, self.last_action_key), 0.0)
        new_q = (1 - self.alpha) * old_q + self.alpha * (
            reward + self.gamma * max_future_q
        )
        self.q_table[(self.last_state_key, self.last_action_key)] = new_q

    # ---------- persistence ----------

    def save_q_table(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self.q_table, f)
        print(f"[DEBUG] Saved Q-table with {len(self.q_table)} entries to {path}")

    def load_q_table(self, path: str) -> None:
        with open(path, "rb") as f:
            self.q_table = pickle.load(f)
        print(f"[DEBUG] Loaded Q-table with {len(self.q_table)} entries from {path}")
