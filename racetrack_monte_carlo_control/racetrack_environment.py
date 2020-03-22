import numpy as np


class Environment:

    def __init__(self, data, gen):
        self.data = data
        self.gen = gen
        self.step_count = 0

    @staticmethod
    def _get_new_state(state, action):
        new_state = state.copy()
        new_state[0] = state[0] - state[2]
        new_state[1] = state[1] + state[3]
        new_state[2] = state[2] + action[0]
        new_state[3] = state[3] + action[1]
        return new_state

    @staticmethod
    def select_randomly(array):
        return np.random.choice(array)

    @staticmethod
    def set_zero(array):

        array[:] = 0
        return array

    def is_finish_line_crossed(self, state, action):
        new_state = self._get_new_state(state, action)
        old_cell, new_cell = state[0:2], new_state[0:2]

        rows = np.array(range(new_cell[0], old_cell[0] + 1))
        cols = np.array(range(old_cell[1], new_cell[1] + 1))
        fin = set([tuple(x) for x in self.data.finish_line])
        row_col_matrix = [(x, y) for x in rows for y in cols]
        intersect = [x for x in row_col_matrix if x in fin]

        return len(intersect) > 0

    def is_out_of_track(self, state, action):

        new_state = self._get_new_state(state, action)
        old_cell, new_cell = state[0:2], new_state[0:2]

        if new_cell[0] < 0 or new_cell[0] >= 100 or new_cell[1] < 0 or new_cell[1] >= 100:
            return True

        else:
            return self.data.racetrack[tuple(new_cell)] == -1

    def reset(self):
        self.data.episode = dict({'S': [], 'A': [], 'probs': [], 'R': [None]})
        self.step_count = 0

    def start(self):
        state = np.zeros(4, dtype='int')
        state[0] = 99
        state[1] = self.select_randomly(self.data.start_line[:, 1])
        return state

    def step(self, state, action):

        self.data.episode['A'].append(action)
        reward = -1

        if self.is_finish_line_crossed(state, action):
            new_state = self._get_new_state(state, action)

            self.data.episode['R'].append(reward)
            self.data.episode['S'].append(new_state)
            self.step_count += 1

            return None, new_state

        elif self.is_out_of_track(state, action):
            new_state = self.start()
        else:
            new_state = self._get_new_state(state, action)

        self.data.episode['R'].append(reward)
        self.data.episode['S'].append(new_state)
        self.step_count += 1

        return reward, new_state