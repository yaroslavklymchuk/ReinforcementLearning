import numpy as np


class Agent:

    def __init__(self):
        pass

    alpha = [(-1, -1), (-1, 0), (0, -1), (-1, 1), (0, 0), (1, -1), (0, 1), (1, 0), (1, 1)]

    def _possible_actions(self, velocity):
        alpha = [np.array(x) for x in self.alpha]

        beta = []
        for i, x in zip(range(9), alpha):
            new_vel = np.add(velocity, x)
            if (new_vel[0] < 5) and (new_vel[0] >= 0) and (new_vel[1] < 5) and (new_vel[1] >= 0) and ~(
                    new_vel[0] == 0 and new_vel[1] == 0):
                beta.append(i)
        beta = np.array(beta)

        return beta

    def _map_to_1d(self, action):
        for i, x in zip(range(9), self.alpha):
            if action[0] == x[0] and action[1] == x[1]:
                return i

    def _map_to_2d(self, action):
        return self.alpha[action]

    def get_action(self, state, policy):
        return self._map_to_2d(policy(state, self._possible_actions(state[2:4])))
