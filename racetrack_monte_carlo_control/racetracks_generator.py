import numpy as np


class Generator:

    def __init__(self):
        pass

    @staticmethod
    def _widen_hole_transformation(racetrack, start_cell, end_cell):

        delta = 1
        while True:
            if (start_cell[1] < delta) or (start_cell[0] < delta):
                racetrack[0:end_cell[0], 0:end_cell[1]] = -1
                break

            if (end_cell[1] + delta > 100) or (end_cell[0] + delta > 100):
                racetrack[start_cell[0]:100, start_cell[1]:100] = -1
                break

            delta += 1

        return racetrack

    @staticmethod
    def _calculate_valid_fraction(racetrack):
        '''
        Returns the fraction of valid cells in the racetrack
        '''
        return len(racetrack[racetrack == 0]) / 10000

    @staticmethod
    def _mark_finish_states(racetrack):
        '''
        Marks finish states in the racetrack
        Returns racetrack
        '''
        last_col = racetrack[0:100, 99]
        last_col[last_col == 0] = 2
        return racetrack

    @staticmethod
    def _mark_start_states(racetrack):
        '''
        Marks start states in the racetrack
        Returns racetrack
        '''
        last_row = racetrack[99, 0:100]
        last_row[last_row == 0] = 1
        return racetrack

    def generate_racetrack(self):
        '''
        racetrack is a 2d numpy array
        codes for racetrack:
            0,1,2 : valid racetrack cells
            -1: invalid racetrack cell
            1: start line cells
            2: finish line cells
        returns randomly generated racetrack
        '''
        racetrack = np.zeros((100, 100), dtype='int')

        frac = 1
        while frac > 0.5:
            # transformation
            random_cell = np.random.randint((100, 100))
            random_hole_dims = np.random.randint((25, 25))
            start_cell = np.array([max(0, x - y // 2) for x, y in zip(random_cell, random_hole_dims)])
            end_cell = np.array([min(100, x + y) for x, y in zip(start_cell, random_hole_dims)])

            # apply_transformation
            racetrack = self._widen_hole_transformation(racetrack, start_cell, end_cell)
            frac = self._calculate_valid_fraction(racetrack)

        racetrack = self._mark_start_states(racetrack)
        racetrack = self._mark_finish_states(racetrack)

        return racetrack


class Data:

    def __init__(self):
        self.load_racetrack()
        self.get_start_line()
        self.get_finish_line()
        self.load_q_vals()
        self.load_c_vals()
        self.load_pi()
        self.load_rewards()
        self.eps = 0.1
        self.gamma = 1
        self.episode = dict({'S': [], 'A': [], 'probs': [], 'R': [None]})

    ROWS = 200
    COLS = 100

    def get_start_line(self):
        self.start_line = np.array([np.array([self.ROWS - 1, j])
                                    for j in range(self.COLS) if self.racetrack[self.ROWS - 1, j] == 1])

    def get_finish_line(self):
        self.finish_line = np.array([np.array([i, self.COLS - 1])
                                     for i in range(self.ROWS) if self.racetrack[i, self.COLS - 1] == 2])

    def save_rewards(self, filename='rewards'):
        self.rewards = np.array(self.rewards)
        np.save(filename, self.rewards)
        self.rewards = list(self.rewards)

    def load_rewards(self):
        self.rewards = list(np.load('rewards.npy'))

    def save_pi(self, filename='pi.npy'):
        np.save(filename, self.pi)

    def load_pi(self):
        self.pi = np.load('π.npy')

    def save_c_vals(self, filename='C_vals.npy'):
        np.save(filename, self.C_vals)

    def load_c_vals(self):
        self.C_vals = np.load('C_vals.npy')

    def save_q_vals(self, filename='Q_vals.npy'):
        np.save(filename, self.Q_vals)

    def load_q_vals(self):
        self.Q_vals = np.load('Q_vals.npy')

    def save_racetrack(self, filename='racetrack.npy'):
        np.save(filename, self.racetrack)

    def load_racetrack(self):
        self.racetrack = np.load('racetrack.npy')