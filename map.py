import pygame
import random
import keyboard

from constant import TILE_SIZE, GRID_SIZE, TileType

# 游戏地图
class Map:
    def __init__(self):
        self.grid = [[TileType.EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.generate_map()

    def generate_map(self):
        # 边缘设置为不可破坏的石块
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if x == 0 or x == GRID_SIZE - 1 or y == 0 or y == GRID_SIZE - 1:
                    self.grid[x][y] = TileType.UNBREAKABLE
                elif x % 2 == 0 and y % 2 == 0:
                    self.grid[x][y] = TileType.UNBREAKABLE
                else:
                    # 随机生成可破坏的石块
                    if random.random() < 0.2:
                        self.grid[x][y] = TileType.BREAKABLE

    def draw(self, screen, tile_img):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[x][y] == TileType.UNBREAKABLE:
                    screen.blit(tile_img[TileType.UNBREAKABLE], (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.BREAKABLE:
                    screen.blit(tile_img[TileType.BREAKABLE], (x * TILE_SIZE, y * TILE_SIZE))