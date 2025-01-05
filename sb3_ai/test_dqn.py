from stable_baselines3 import DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from env import BombermanEnv

def test_dqn_model():
    #創建環境
    env = DummyVecEnv([lambda: BombermanEnv(render_mode="human")])

    # 載入DQN模型
    model = DQN.load("saved_models/bomberman_dqn_ai")

    obs = env.reset()
    done = False
    reward_list = []

    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        reward_list.append(reward)
        print(f"Action: {action}, Reward: {reward}")
        env.render()

    print("Test completed!")
