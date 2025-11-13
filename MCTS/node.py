from wingedsheep.carcassonne.carcassonne_game import CarcassonneGameState
from wingedsheep.carcassonne.objects.actions.action import Action
from wingedsheep.carcassonne.objects.actions.tile_action import TileAction
from wingedsheep.carcassonne.utils.action_util import ActionUtil
from wingedsheep.carcassonne.utils.state_updater import StateUpdater

from typing import Dict

import random
import math

class MCTSNode:
    def __init__(self, state: CarcassonneGameState, exploration_rate: 0.3, parent: 'MCTSNode' =None):
        self.state: CarcassonneGameState = state
        self.exploration_rate = exploration_rate
        self.parent: MCTSNode = parent
        self.children: Dict[Action, state] = {}
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.get_possible_actions())

    def get_possible_actions(self):
        return ActionUtil.get_possible_actions(self.state)

    def select_expand(self):
        # Select base on score
        curr_max_q = float('-inf')
        explore = random.random() < self.exploration_rate
        if len(self.children) == 0 or (explore and not self.is_fully_expanded()):
            untried_actions = [action for action in self.get_possible_actions() if action not in self.children]
            action = random.choice(untried_actions)
            new_state = StateUpdater.apply_action(self.state, action)
            new_node = MCTSNode(state=new_state, exploration_rate=self.exploration_rate, parent=self)
            self.children[action] = new_node
            return new_node
        else:
            selected_action = None
            for action, state in self.children.items():
                q = state.wins / state.visits + (2 * (2 * math.log(self.visits) / state.visits) ) ** 0.5
                if q > curr_max_q:
                    curr_max_q = q
                    selected_action = action
            curr_node = self.children[selected_action]
            return curr_node.select_expand()

    def rollout(self):
        current_state = self.state
        while not current_state.is_terminated():
            # print(f"Remaining tiles: {len(current_state.deck)}")
            possible_actions = ActionUtil.get_possible_actions(current_state)
            action = random.choice(possible_actions)
            current_state = StateUpdater.apply_action(current_state, action)
        return current_state

    def update(self, win: bool, result: int):
        self.visits += 1
        # TODO: update wins based on result
        if win:
            self.wins += 1
            # TODO: complex scoring
        if self.parent:
            if self.get_possible_actions()[0] is TileAction:
                self.parent.update(not win, -result)
            else:
                self.parent.update(win, result)