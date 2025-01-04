# import gymnasium as gym
# from gymnasium import spaces
# import numpy as np
# from stable_baselines3 import PPO

# from constant import *
# from map import Map
# from player import Player

# class BombermanEnv(gym.Env):
#     def __init__(self):
#         super(BombermanEnv, self).__init__()
#         self.map_instance = Map()  # 使用外部传入的地图实例，默认创建一个新的Map
#         self.observation_space = spaces.Box(low=0, high=255, shape=(GRID_SIZE, GRID_SIZE, 5), dtype=np.uint8)
#         self.action_space = spaces.Discrete(6)  # 动作为上下左右和放炸弹
#         self.reset()

#     def reset(self):
#         # 重置地图
#         self.map_instance.generate_map()
#         self.state = self.map_instance.grid
#         self.done = False
#         # 玩家初始位置
#         self.player_pos = [(1, 1), (GRID_SIZE - 2, GRID_SIZE - 2)]
#         return self._get_observation()
    
#     def step(self, action):
#         # 玩家移动逻辑
#         for idx in enumerate(self.player_pos):
#              # 根据动作更新dx, dy
#             if action == 0:  # 上
#                 dx, dy = -1, 0
#             elif action == 1:  # 下
#                 dx, dy = 1, 0
#             elif action == 2:  # 左
#                 dx, dy = 0, -1
#             elif action == 3:  # 右
#                 dx, dy = 0, 1
#             elif action == 4:  # 放置炸弹（示例，需扩展逻辑）
#                 self.map_instance.place_bomb(x, y)
#                 continue
            
#             # 使用 Player 类的 move 方法进行位置更新
#             moved = Player.move(dx, dy, self.state)
#             if moved:
#                 self.player_pos[idx] = moved
#             if not moved:
#                 rewards -= 1  # 碰撞，给予负奖励

#     def render(self, mode="human"):
#         # 简单的文字渲染
#         print("\n".join("".join(str(cell) for cell in row) for row in self.state))
#         print(f"Player positions: {self.player_pos}")

#     def _get_observation(self):
#         obs = self.state.copy()
#         for idx, pos in enumerate(self.player_pos):
#             obs[pos] = 2 + idx  # 玩家位置标记
#         return obs

# class MultiAgentBombermanEnv(BombermanEnv):
#     def __init__(self):
#         super(MultiAgentBombermanEnv, self).__init__()
#         self.map_instance = Map()  # 使用外部传入的地图实例，默认创建一个新的Map
#         self.num_agents = 2

#         self.action_space = spaces.MultiDiscrete([6] * self.num_agents)  # 每个智能体有5个动作
#         self.observation_space = spaces.Tuple(
#             [spaces.Box(low=0, high=255, shape=(GRID_SIZE, GRID_SIZE), dtype=np.uint8) for _ in range(self.num_agents)]
#         )

#         self.reset()

#     def step(self, actions):
#         """
#         actions: list of actions for all agents.
#         """
#         rewards = [0] * self.num_agents
#         self.done = False

#         # 处理每个智能体的动作
#         for agent_idx, action in enumerate(actions):
#             x, y = self.agent_positions[agent_idx]
#             dx, dy = 0, 0

#             # 根据动作更新dx, dy
#             if action == 0:  # 上
#                 dx, dy = -1, 0
#             elif action == 1:  # 下
#                 dx, dy = 1, 0
#             elif action == 2:  # 左
#                 dx, dy = 0, -1
#             elif action == 3:  # 右
#                 dx, dy = 0, 1
#             elif action == 4:  # 放置炸弹（示例，需扩展逻辑）
#                 self.map_instance.place_bomb(x, y)
#                 continue

#             # 使用 Player 类的 move 方法进行位置更新
#             moved = self.players[agent_idx].move(dx, dy, self.state)
#             if not moved:
#                 rewards[agent_idx] -= 1  # 碰撞，给予负奖励

#         # 判断游戏是否结束
#         self.done = self.map_instance.is_finished

#         return self._get_observations(), rewards, self.done, {}

#     def reset(self):
#         # 重置地图和智能体位置
#         self.map_instance.generate_map()
#         self.state = np.array(self.map_instance.grid)
#         self.agent_positions = [(1, 1), (GRID_SIZE - 2, GRID_SIZE - 2)]  # 智能体初始位置
#         self.done = False

#         return self._get_observations()
    
#     def _get_observations(self):
#         # 每个智能体返回相同的全局地图观察（可以改为局部视野）
#         return [self.state.copy() for _ in range(self.num_agents)]


# # 初始化环境
# env = MultiAgentBombermanEnv(map_size=(10, 10))

# # 初始化两个AI模型
# model_1 = PPO("MlpPolicy", env, verbose=1)
# model_2 = PPO("MlpPolicy", env, verbose=1)

# # 训练模型
# for _ in range(10000):  # 训练轮数
#     obs = env.reset()
#     done = False
#     while not done:
#         action_1 = model_1.predict(obs[0])[0]  # AI 1的动作
#         action_2 = model_2.predict(obs[1])[0]  # AI 2的动作
#         obs, rewards, done, _ = env.step([action_1, action_2])
#         model_1.learn(rewards[0])
#         model_2.learn(rewards[1])

# # 测试两个AI的对战
# obs = env.reset()
# done = False
# while not done:
#     action_1 = model_1.predict(obs[0])[0]
#     action_2 = model_2.predict(obs[1])[0]
#     obs, rewards, done, _ = env.step([action_1, action_2])
#     env.render()
