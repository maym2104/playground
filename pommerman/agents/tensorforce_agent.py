"""
A Work-In-Progress agent using Tensorforce
"""
from . import BaseAgent
from .. import characters


class TensorForceAgent(BaseAgent):
    """The TensorForceAgent. Acts through the algorithm, not here."""

    def __init__(self, character=characters.Bomber, algorithm='ppo'):
        super(TensorForceAgent, self).__init__(character)
        self.algorithm = algorithm

    def act(self, obs, action_space):
        """This agent has its own way of inducing actions. See train_with_tensorforce."""
        return None

    def initialize(self, env, lstm=False):
        from gym import spaces
        from tensorforce.agents import PPOAgent

        if self.algorithm == "ppo":
            if type(env.action_space) == spaces.Tuple:
                actions = {
                    str(num): {
                        'type': int,
                        'num_actions': space.n
                    }
                    for num, space in enumerate(env.action_space.spaces)
                }
            else:
                actions = dict(type='int', num_actions=env.action_space.n)

            network = [
                    dict(type='conv2d', size=10, window=1, activation='relu'),
                    dict(type='conv2d', size=32, window=5, activation='relu'),
                    dict(type='conv2d', size=16, window=3, activation='relu'),
                    dict(type='flatten'),
                    dict(type='dense', size=256, activation='relu')
                ]

            if lstm:
                network.append(dict(type='internal_lstm', size=256))

            return PPOAgent(
                states=dict(type='float', shape=env.observation_space.shape),
                actions=actions,
                network=network,
                batching_capacity=1000,
                step_optimizer=dict(type='adam', learning_rate=1e-4))
        return None
