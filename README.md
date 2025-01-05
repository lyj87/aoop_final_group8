# Bomberman 轟炸超人

## 簡介
轟炸超人是一款非常經典的遊戲，已經有40年的歷史，玩家需要穿越迷宮，用炸彈破壞障礙物。最後，通過策略性地放置炸彈擊敗敵人或其他玩家。

### 主要特點：
- 雙人模式：與朋友競爭
- 隨機環境：隨機地圖、隨機增益
- 新技能：除了傳統炸彈，現在玩家還可以製造障礙物

## 安裝
Clone the repository
```
https://github.com/lyj87/aoop_final_group8.git
```

Navigate to the project directory
```
cd ./path/aoop_final_group8
```

Install the required dependencies
```
pip install pygame
```
Run the game
```
python main.py
```

## 玩法
- 開始界面

  輸入玩家一的名字，按Tab，可輸入另外一個玩家的名字，都輸入完成後，可按enter進入遊戲
  
- 游戲界面

   玩家一通過WASD控制角色移動，q是放炸彈，e是製造障礙物

   玩家二通過上下左右鍵控制角色移動，shift是放炸彈，'/'是製造障礙物

- gameover界面

  按r可重新遊玩
  按p回到開始界面

## 作者
TJKAI00  https://github.com/TJKAI00

## 授權
MIT

## 參考圖片
https://opengameart.org/content/bomb-party-the-complete-set

https://www.freepik.com/premium-vector/pixel-art-explosion-icon-retro-8-bit-style-burst-illustration-gaming-graphics_285202478.htm

https://www.istockphoto.com/vector/vector-pixel-art-isolated-bomb-blast-gm1208336101-349219477

https://kenmi-art.itch.io/cute-fantasy-rpg

https://www.freepik.com/premium-vector/bomb-pixel-art-style_22989300.htm

https://www.vecteezy.com/vector-art/24693834-pixel-art-heart-love-and-valentine

# stable baselines3

## 簡介

Stable Baselines3 是一個基於 Python 的開源深度強化學習框架，專為研究和應用強化學習（Reinforcement Learning, RL）算法而設計。它是原始 Stable Baselines 的重寫版，改用 PyTorch 作為深度學習框架，提供更現代化、更易於擴展和維護的架構。

### 主要特點

- 多種算法支持：Stable Baselines3 提供多種主流強化學習算法的實現，包括 DQN、PPO、A2C、SAC、TD3 等，方便用戶快速上手和應用不同的算法。

- 易於使用：該框架旨在降低強化學習的入門門檻，通過簡單的 API，使用者可以快速定義和訓練模型。

- 模組化：架構設計模組化，允許用戶輕鬆擴展和自定義算法、環境、策略等。

## 用法

Install the required dependencies
```
pip install gymnasium
pip install stable-baselines3
```

注意不要pip install gym ，這個是老版本，python 也不要太新，截至2025年1月5日，推薦使用的python版本為3.12.8及以前，不要安裝3.13的

主要任務是編寫env.py檔案，設置環境與獎勵

## 參考鏈接

https://github.com/DLR-RM/stable-baselines3

https://stable-baselines3.readthedocs.io/en/master/
