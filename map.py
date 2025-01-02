import random
from constant import *

# 游戏地图
class Map:
    def __init__(self):
        self.grid = [[TileType.EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.generate_map()
        self.shrink_count = 0  # 缩小次数计数
        self.timer = 150  # 爆炸倒计时 5 秒（30 幀/秒）

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
                        self.grid[GRID_SIZE - 1 - x][GRID_SIZE - 1 - y] = TileType.BREAKABLE

       # 角色周围没有炸弹
        for y in range(1, 3):
            for x in range(1, 3):
                if self.grid[x][y] == TileType.BREAKABLE:
                    self.grid[x][y] = TileType.EMPTY
 
        # 角色周围没有炸弹
        for y in range(GRID_SIZE - 3, GRID_SIZE - 1):
            for x in range(GRID_SIZE - 3, GRID_SIZE - 1):
                if self.grid[x][y] == TileType.BREAKABLE:
                    self.grid[x][y] = TileType.EMPTY

        # 随机生成BUFF
        buff_num_count = 0
        while buff_num_count < 4:
            x = random.randint(1, GRID_SIZE - 2)
            y = random.randint(1, GRID_SIZE - 2)
            if self.grid[x][y] == TileType.BREAKABLE:
                self.grid[x][y] = TileType.GRASS_BUFF_NUM
                buff_num_count += 1
                print(f"BUFF_NUM: {buff_num_count} at ({x}, {y})")

        buff_range_count = 0
        while buff_range_count < 4:
            x = random.randint(1, GRID_SIZE - 2)
            y = random.randint(1, GRID_SIZE - 2)
            if self.grid[x][y] == TileType.BREAKABLE and self.grid[x][y] != TileType.GRASS_BUFF_NUM:
                self.grid[x][y] = TileType.GRASS_BUFF_RANGE
                buff_range_count += 1
                print(f"BUFF_RANGE: {buff_range_count} at ({x}, {y})")

        heal_count = 0
        while heal_count < 4:
            x = random.randint(1, GRID_SIZE - 2)
            y = random.randint(1, GRID_SIZE - 2)
            if self.grid[x][y] == TileType.BREAKABLE and self.grid[x][y] != TileType.GRASS_BUFF_NUM and self.grid[x][y] != TileType.GRASS_BUFF_RANGE:
                self.grid[x][y] = TileType.GRASS_HEAL
                heal_count += 1
                print(f"HEAL: {heal_count} at ({x}, {y})")

    # def shrink_map(self):
    #     # 缩小地图边界
    #     if self.timer > 0 and GRID_SIZE // 2 > self.shrink_count:  # 确保不会缩小到中心点
    #         layer = self.shrink_count
    #         self.timer -= 1
    #         for i in range(layer, GRID_SIZE - layer):
    #             self.grid[layer][i] = TileType.AROUND
    #             self.grid[GRID_SIZE - 1 - layer][i] = TileType.AROUND
    #             if i != layer:
    #                 self.grid[i][layer] = TileType.UNBREAKABLE
    #             self.grid[i][GRID_SIZE - 1 - layer] = TileType.UNBREAKABLE
    #         self.shrink_count += 1
    #         print(f"Map shrunk to layer {self.shrink_count}")

    def draw(self, screen, tile_img):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[x][y] == TileType.UNBREAKABLE:
                    screen.blit(tile_img[TileType.UNBREAKABLE], (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.BREAKABLE:
                    screen.blit(tile_img[TileType.BREAKABLE], (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.AROUND:
                    screen.blit(tile_img[TileType.AROUND], (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.BUFF_RANGE:
                    screen.blit(tile_img[TileType.BUFF_RANGE], (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.BUFF_NUM:
                    screen.blit(tile_img[TileType.BUFF_NUM], (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.HEAL:
                    screen.blit(tile_img[TileType.HEAL], (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.GRASS_BUFF_RANGE:
                    screen.blit(tile_img[TileType.BREAKABLE], (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.GRASS_BUFF_NUM:
                    screen.blit(tile_img[TileType.BREAKABLE], (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.GRASS_HEAL:
                    screen.blit(tile_img[TileType.BREAKABLE], (x * TILE_SIZE, y * TILE_SIZE))