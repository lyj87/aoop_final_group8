import gymnasium as gym
from gymnasium import spaces
import numpy as np
from map import generate_map
import matplotlib.pyplot as plt

# 定義一個自訂的炸彈人遊戲環境
class BombermanEnv(gym.Env):
    def __init__(self, render_mode=None):
        super(BombermanEnv, self).__init__()
        self.size = 13  # # 遊戲地圖的大小
        self.action_space = spaces.Discrete(5)  # 定義5個可能的動作（上、下、左、右、放置炸彈）
        self.observation_space = spaces.Box(
            low=0, high=3, shape=(self.size, self.size), dtype=int  # # 觀察空間是一個值為0到3的三維空間
        )
        self.render_mode = render_mode  # 渲染模式，默認無
        self.seed() # 初始化隨機數生成器
        self.last_bomb_reward = 0

    def seed(self, seed=None):
        # 設置隨機種子
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        return [seed]

    def reset(self, seed=None, options=None):
        # 如果提供種子，重置種子
        if seed is not None:
            self.seed(seed)
        self.game_map = generate_map(self.size)
        self.player_pos = [1, 1]
        self.last_bomb_reward = 0
        return self.get_observation(), {}

    def step(self, action):
        reward = 0  # 初始化獎勵
        terminated = False  # 初始化終止標誌
        truncated = False  # 初始化截斷標誌
        info = {}   # 初始化信息

        # 上下左右
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
            reward += 100       # 抵達右下角，獎勵+100
            terminated = True   # 遊戲結束

        return self.get_observation(), reward, terminated, truncated, info

    def move(self, dx, dy):
        new_x = self.player_pos[0] + dx # 新的x座標
        new_y = self.player_pos[1] + dy # 新的y座標
        if self.game_map[new_x, new_y] == 0:    # 如果新的位置是空的
            self.player_pos = [new_x, new_y]    # 更新玩家位置

    def place_bomb(self):
        x, y = self.player_pos
        bomb_reward = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.game_map[nx, ny] == 2:
                self.game_map[nx, ny] = 0
                bomb_reward += 1 # 增加炸彈獎勵
        self.last_bomb_reward = bomb_reward
        return bomb_reward

    def get_observation(self):
        obs = self.game_map.copy()
        obs[self.player_pos[0], self.player_pos[1]] = 3  # 玩家位置
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