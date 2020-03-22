from .agents import Agent
from .visualize_results import Visualizer
from .monte_carlo_control import MonteCarloControl
from .racetrack_environment import Environment
from .racetracks_generator import Generator, Data


def main():
    data = Data()
    gen = Generator()
    env = Environment(data, gen)
    mcc = MonteCarloControl(data)
    vis = Visualizer(data)
    agent = Agent()

    vis.visualize_racetrack()

    for i in range(50000):
        mcc.control(env, agent)

        if i%10 == 9:
            mcc.evaluate_target_policy(agent=agent, env=env)

        if i%100 == 99:
            mcc.save_your_work()
            mcc.plot_rewards()
