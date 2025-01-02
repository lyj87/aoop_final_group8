import pygame

# 常量定义
TILE_SIZE = 32
GRID_SIZE = 23  # 游戏地图的网格大小
IMG_SIZE = 32
SCOREBOARD_WIDTH = 250  # 计分板宽度
SCREEN_WIDTH = GRID_SIZE * TILE_SIZE + SCOREBOARD_WIDTH
SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 石块类型
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

player_img = pygame.image.load("./assets/player.png")
player_frames = {
    "DOWN": [],
    "RIGHT": [],
    "LEFT": [],
    "UP": []
}
for i in range(6):  # 6 frames per direction
    player_frames["DOWN"].append(player_img.subsurface((i * IMG_SIZE, 3 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))
    player_frames["RIGHT"].append(player_img.subsurface((i * IMG_SIZE, 4 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))
    player_frames["LEFT"].append(pygame.transform.flip(player_img.subsurface((i * IMG_SIZE, 4 * IMG_SIZE, IMG_SIZE, IMG_SIZE)), True, False))
    player_frames["UP"].append(player_img.subsurface((i * IMG_SIZE, 5 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))

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


assets_img = pygame.image.load("./assets/assets.png")

background_img = assets_img.subsurface(1 * IMG_SIZE, 3 * IMG_SIZE, IMG_SIZE, IMG_SIZE)
background_img = pygame.transform.scale(background_img, (TILE_SIZE, TILE_SIZE))

tile_around_img = assets_img.subsurface(10 * IMG_SIZE, 18 * IMG_SIZE, IMG_SIZE, IMG_SIZE)
tile_around_img = pygame.transform.scale(tile_around_img, (TILE_SIZE, TILE_SIZE))

tile_unbreakable_img = assets_img.subsurface(10 * IMG_SIZE, 17 * IMG_SIZE, IMG_SIZE, IMG_SIZE)
tile_unbreakable_img = pygame.transform.scale(tile_unbreakable_img, (TILE_SIZE, TILE_SIZE))

tile_breakable_img = assets_img.subsurface(3 * IMG_SIZE, 13 * IMG_SIZE, IMG_SIZE, IMG_SIZE)
tile_breakable_img = pygame.transform.scale(tile_breakable_img, (TILE_SIZE, TILE_SIZE))

tile_buff_num_img = pygame.image.load("./assets/icon_bomb_num.png")
tile_buff_num_img = pygame.transform.scale(tile_buff_num_img, (TILE_SIZE, TILE_SIZE))

tile_buff_range_img = pygame.image.load("./assets/icon_bomb_range.png")
tile_buff_range_img = pygame.transform.scale(tile_buff_range_img, (TILE_SIZE, TILE_SIZE))

tile_heal_img = pygame.image.load("./assets/icon_heal.png")
tile_heal_img = pygame.transform.scale(tile_heal_img, (TILE_SIZE, TILE_SIZE))

water_img = pygame.image.load("./assets/water.png")
tile_water_img = water_img.subsurface(2 * IMG_SIZE, 13 * IMG_SIZE, IMG_SIZE, IMG_SIZE)
tile_water_img = pygame.transform.scale(tile_water_img, (TILE_SIZE, TILE_SIZE))