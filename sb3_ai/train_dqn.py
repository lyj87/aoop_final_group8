from stable_baselines3 import DQN
from env import BombermanEnv

def train_dqn_model():
    env = BombermanEnv()
    model = DQN("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100000)
    model.save("saved_models/bomberman_dqn_ai")
    print("Model trained and saved.")

if __name__ == "__main__":
    train_dqn_model()