from stable_baselines3 import PPO
from env import BombermanEnv

def train_model():
    env = BombermanEnv()
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=100000)
    model.save("saved_models/bomberman_ai")
    print("Model trained and saved.")

if __name__ == "__main__":
    train_model()