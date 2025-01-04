import pygame

# 常量定义
TILE_SIZE = 32  # 磚塊大小
GRID_SIZE = 19  # 磚塊數量，地圖大小
IMG_SIZE = 32
SCOREBOARD_WIDTH = 250  # 計分板寬度
GAME_HEIGHT = GRID_SIZE * TILE_SIZE # 游戲視窗高度（不包含計分板）
GAME_WIDTH = GRID_SIZE * TILE_SIZE  # 游戲視窗寬度（不包含計分板）
SCREEN_WIDTH = GRID_SIZE * TILE_SIZE + SCOREBOARD_WIDTH # 視窗寬度
SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE   # 視窗高度

SHRINK_COUNT = 1800  # 縮小地圖的倒計時 60 秒（30 幀/秒）

# 顔色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 磚塊類型
class TileType:
    UNBREAKABLE = 0
    BREAKABLE = 1
    EMPTY = 2
    AROUND = 3
    BUFF_RANGE = 4
    BUFF_NUM = 5
    HEAL = 6
    GRASS_BUFF_RANGE = 7
    GRASS_BUFF_NUM = 8
    GRASS_HEAL = 9
    BOMB = 10
    WATER = 11

# player1 圖片
player_img = pygame.image.load("./assets/player.png")
player1_frames = {
    "DOWN": [],
    "RIGHT": [],
    "LEFT": [],
    "UP": []
}
for i in range(6):  # 6 frames per direction
    player1_frames["DOWN"].append(player_img.subsurface((i * IMG_SIZE, 3 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))
    player1_frames["RIGHT"].append(player_img.subsurface((i * IMG_SIZE, 4 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))
    player1_frames["LEFT"].append(pygame.transform.flip(player_img.subsurface((i * IMG_SIZE, 4 * IMG_SIZE, IMG_SIZE, IMG_SIZE)), True, False))
    player1_frames["UP"].append(player_img.subsurface((i * IMG_SIZE, 5 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))

# player2 圖片
player2_img = pygame.image.load("./assets/player2.png")
player2_frames = {
    "DOWN": [],
    "RIGHT": [],
    "LEFT": [],
    "UP": []
}
for i in range(6):  # 6 frames per direction
    player2_frames["DOWN"].append(player2_img.subsurface((i * IMG_SIZE, 3 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))
    player2_frames["RIGHT"].append(player2_img.subsurface((i * IMG_SIZE, 4 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))
    player2_frames["LEFT"].append(pygame.transform.flip(player2_img.subsurface((i * IMG_SIZE, 4 * IMG_SIZE, IMG_SIZE, IMG_SIZE)), True, False))
    player2_frames["UP"].append(player2_img.subsurface((i * IMG_SIZE, 5 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))

# 受傷角色圖片
damage_player_img = pygame.image.load("./assets/damage_player.png")
damage_player_frames = {
    "DOWN": [],
    "RIGHT": [],
    "LEFT": [],
    "UP": []
}
for i in range(6):  # 6 frames per direction
    damage_player_frames["DOWN"].append(damage_player_img.subsurface((i * IMG_SIZE, 3 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))
    damage_player_frames["RIGHT"].append(damage_player_img.subsurface((i * IMG_SIZE, 4 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))
    damage_player_frames["LEFT"].append(pygame.transform.flip(damage_player_img.subsurface((i * IMG_SIZE, 4 * IMG_SIZE, IMG_SIZE, IMG_SIZE)), True, False))
    damage_player_frames["UP"].append(damage_player_img.subsurface((i * IMG_SIZE, 5 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))

# 炸彈圖片
bomb_img = pygame.image.load("./assets/assets.png")
bomb_frames = []
for i in range(4, 10):
    bomb_frames.append(bomb_img.subsurface((i * IMG_SIZE, 18 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))

# 主要素材圖片
assets_img = pygame.image.load("./assets/assets.png")

# 爆炸圖片
explosion_img = pygame.image.load("./assets/explosion.png")
explosion_img = pygame.transform.scale (explosion_img, (TILE_SIZE, TILE_SIZE))

# empty地圖圖片
background_img = assets_img.subsurface(1 * IMG_SIZE, 3 * IMG_SIZE, IMG_SIZE, IMG_SIZE)
background_img = pygame.transform.scale(background_img, (TILE_SIZE, TILE_SIZE))

# 磚塊圖片（不可破壞）
tile_around_img = assets_img.subsurface(10 * IMG_SIZE, 18 * IMG_SIZE, IMG_SIZE, IMG_SIZE)
tile_around_img = pygame.transform.scale(tile_around_img, (TILE_SIZE, TILE_SIZE))

# 磚塊圖片（不可破壞）
tile_unbreakable_img = assets_img.subsurface(10 * IMG_SIZE, 17 * IMG_SIZE, IMG_SIZE, IMG_SIZE)
tile_unbreakable_img = pygame.transform.scale(tile_unbreakable_img, (TILE_SIZE, TILE_SIZE))

# 草堆圖片（可破壞）
tile_breakable_img = assets_img.subsurface(3 * IMG_SIZE, 13 * IMG_SIZE, IMG_SIZE, IMG_SIZE)
tile_breakable_img = pygame.transform.scale(tile_breakable_img, (TILE_SIZE, TILE_SIZE))

# 炸彈數量 buff 圖片
tile_buff_num_img = pygame.image.load("./assets/icon_bomb_num.png")
tile_buff_num_img = pygame.transform.scale(tile_buff_num_img, (TILE_SIZE, TILE_SIZE))

# 炸彈範圍 buff 圖片
tile_buff_range_img = pygame.image.load("./assets/icon_bomb_range.png")
tile_buff_range_img = pygame.transform.scale(tile_buff_range_img, (TILE_SIZE, TILE_SIZE))

# 生命值圖片
tile_heal_img = pygame.image.load("./assets/icon_heal.png")
tile_heal_img = pygame.transform.scale(tile_heal_img, (TILE_SIZE, TILE_SIZE))

# 水圖片
water_img = pygame.image.load("./assets/water.png")
tile_water_img = water_img.subsurface(2 * IMG_SIZE, 13 * IMG_SIZE, IMG_SIZE, IMG_SIZE)
tile_water_img = pygame.transform.scale(tile_water_img, (TILE_SIZE, TILE_SIZE))

# 開始畫面
start_img = pygame.image.load("./assets/start.jpg")
start_img = pygame.transform.scale(start_img, (SCREEN_WIDTH, SCREEN_HEIGHT))