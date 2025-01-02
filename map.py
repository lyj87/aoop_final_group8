import pygame
import random
import keyboard
from constant import *


# 游戏地图
class Map:
    def __init__(self):
        self.grid = [[TileType.EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.generate_map()

    def generate_map(self):
        # 边缘设置为不可破坏的石块
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                # 设置边缘
                if (x == 0 or x == GRID_SIZE - 1) and y != GRID_SIZE - 1:
                    self.grid[x][y] = TileType.AROUND
                elif y == 0 or y == GRID_SIZE - 1:
                    self.grid[x][y] = TileType.UNBREAKABLE
                # 设置偶数坐标为不可破坏石块
                elif x % 2 == 0 and y % 2 == 0 and not (x == GRID_SIZE-2 and y == GRID_SIZE-2):
                    self.grid[x][y] = TileType.UNBREAKABLE
                else:
                    # 随机生成可破坏的石块
                    if random.random() < 0.2 and not (x == 1 and y == 1) and not (x == GRID_SIZE-2 and y == GRID_SIZE-2):
                    # 随机生成可破坏的石块，并对称设置
                    # 设置当前点为BREAKABLE
                        self.grid[x][y] = TileType.BREAKABLE
       # 角色周围没有炸弹
        for y in range(1, 3):
            for x in range(1, 3):
                if self.grid[x][y] == TileType.BREAKABLE:
                    self.grid[x][y] = TileType.EMPTY
 
        # 角色周围没有炸弹
        for y in range(18, 20):
            for x in range(18, 20):
                if self.grid[x][y] == TileType.BREAKABLE:
                    self.grid[x][y] = TileType.EMPTY

    def draw(self, screen, tile_img):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[x][y] == TileType.UNBREAKABLE:
                    screen.blit(tile_img[TileType.UNBREAKABLE], (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.BREAKABLE:
                    screen.blit(tile_img[TileType.BREAKABLE], (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.AROUND:
                    screen.blit(tile_img[TileType.AROUND], (x * TILE_SIZE, y * TILE_SIZE))