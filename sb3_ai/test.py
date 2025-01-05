from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from env import BombermanEnv

def test_model():
    env = DummyVecEnv([lambda: BombermanEnv(render_mode="human")])
    model = PPO.load("saved_models/bomberman_ai")

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