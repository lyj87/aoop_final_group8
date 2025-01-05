import gymnasium as gym
from gymnasium import spaces
import numpy as np
from map import generate_map
import matplotlib.pyplot as plt

class BombermanEnv(gym.Env):
    def __init__(self, render_mode=None):
        super(BombermanEnv, self).__init__()
        self.size = 13
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(
            low=0, high=3, shape=(self.size, self.size), dtype=int
        )
        self.render_mode = render_mode
        self.seed()
        self.last_bomb_reward = 0

    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def reset(self, seed=None, options=None):
        if seed is not None:
            self.seed(seed)
        self.game_map = generate_map(self.size)
        self.player_pos = [1, 1]
        self.last_bomb_reward = 0
        return self.get_observation(), {}

    def step(self, action):
        reward = 0
        terminated = False
        truncated = False
        info = {}

        if action == 0:
            self.move(-1, 0)
        elif action == 1:
            self.move(1, 0)
        elif action == 2:
            self.move(0, -1)
        elif action == 3:
            self.move(0, 1)
        elif action == 4:
            reward += self.place_bomb()

        if self.player_pos == [self.size - 2, self.size - 2]:
            reward += 100
            terminated = True

        return self.get_observation(), reward, terminated, truncated, info

    def move(self, dx, dy):
        new_x = self.player_pos[0] + dx
        new_y = self.player_pos[1] + dy
        if self.game_map[new_x, new_y] == 0:
            self.player_pos = [new_x, new_y]

    def place_bomb(self):
        x, y = self.player_pos
        bomb_reward = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.game_map[nx, ny] == 2:
                self.game_map[nx, ny] = 0
                bomb_reward += 1
        self.last_bomb_reward = bomb_reward
        return bomb_reward

    def get_observation(self):
        obs = self.game_map.copy()
        obs[self.player_pos[0], self.player_pos[1]] = 3
        return obs
        
    def render(self, mode="human"):
        if self.render_mode is None:
            return

        obs = self.get_observation()
        plt.imshow(obs, cmap='hot', interpolation='nearest')
        plt.colorbar()

        if hasattr(self, 'player_path') and len(self.player_path) > 0:
            path_array = np.array(self.player_path)
            plt.plot(path_array[:, 1], path_array[:, 0], marker='o', color='blue', markersize=3, label="Player Path")
            plt.legend()

        plt.title(f"Player Position: {self.player_pos}")
        plt.show(block=False)
        plt.pause(0.1)
        plt.clf()