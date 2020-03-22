import matplotlib.pyplot as plt
import numpy as np


class MonteCarloControl:

    def __init__(self, data):
        self.data = data
        for i in range(100):
            for j in range(100):
                if self.data.racetrack[i, j] != -1:
                    for k in range(5):
                        for l in range(5):
                            self.data.pi[i, j, k, l] = np.argmax(self.data.Q_vals[i, j, k, l])

    def evaluate_target_policy(self, env, agent):
        env.reset()
        state = env.start()
        self.data.episode['S'].append(state)
        rew = -1
        while rew:
            action = agent.get_action(state, self.generate_target_policy_action)
            rew, state = env.step(state, action)

        self.data.rewards.append(sum(self.data.episode['R'][1:]))

    def plot_rewards(self):
        ax, fig = plt.subplots(figsize=(30, 15))
        x = np.arange(1, len(self.data.rewards) + 1)
        plt.plot(x * 10, self.data.rewards, linewidth=0.5, color='#BB8FCE')
        plt.xlabel('Episode number', size=20)
        plt.ylabel('Reward', size=20)
        plt.title('Plot of Reward vs Episode Number', size=20)
        plt.xticks(size=20)
        plt.yticks(size=20)
        plt.savefig('RewardGraph.png')
        plt.close()

    def save_your_work(self):
        self.data.save_q_vals()
        self.data.save_c_vals()
        self.data.save_pi()
        self.data.save_rewards()

    def determine_probability_behaviour(self, state, action, possible_actions):
        best_action = self.data.pi[tuple(state)]
        num_actions = len(possible_actions)

        if best_action in possible_actions:
            if action == best_action:
                prob = 1 - self.data.eps + self.data.eps / num_actions
            else:
                prob = self.data.eps / num_actions
        else:
            prob = 1 / num_actions

        self.data.episode['probs'].append(prob)

    def generate_target_policy_action(self, state, possible_actions):
        if self.data.pi[tuple(state)] in possible_actions:
            action = self.data.pi[tuple(state)]
        else:
            action = np.random.choice(possible_actions)

        return action

    def generate_behavioural_policy_action(self, state, possible_actions):
        if np.random.rand() > self.data.eps and self.data.pi[tuple(state)] in possible_actions:
            action = self.data.pi[tuple(state)]
        else:
            action = np.random.choice(possible_actions)

        self.determine_probability_behaviour(state, action, possible_actions)

        return action

    def control(self, env, agent):
        env.reset()
        state = env.start()
        self.data.episode['S'].append(state)
        rew = -1
        while rew:
            action = agent.get_action(state, self.generate_behavioural_policy_action)
            rew, state = env.step(state, action)

        G = 0
        W = 1
        T = env.step_count

        for t in range(T - 1, -1, -1):
            G = self.data.gamma * G + self.data.episode['R'][t + 1]
            S_t = tuple(self.data.episode['S'][t])
            A_t = agent.map_to_1D(self.data.episode['A'][t])

            S_list = list(S_t)
            S_list.append(A_t)
            SA = tuple(S_list)

            self.data.C_vals[SA] += W
            self.data.Q_vals[SA] += (W * (G - self.data.Q_vals[SA])) / (self.data.C_vals[SA])
            self.data.pi[S_t] = np.argmax(self.data.Q_vals[S_t])
            if A_t != self.data.pi[S_t]:
                break
            W /= self.data.episode['probs'][t]