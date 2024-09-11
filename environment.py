import gym
from gym import spaces
import numpy as np

class PersonalityEnv(gym.Env):
    def __init__(self):
        super(PersonalityEnv, self).__init__()
        self.action_space = spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(1,), dtype=np.float32)
        self.current_state = 0.5  # Example: mood starts at neutral

    def step(self, action):
        # Example: Adjust mood state based on action
        self.current_state += action[0] * 0.1  # Adjust mood
        reward = -abs(self.current_state - 0.5)  # Closer to 0.5 = better reward
        done = False
        return np.array([self.current_state]), reward, done, {}

    def reset(self):
        self.current_state = 0.5
        return np.array([self.current_state])
