import random
from constant import *

# 地圖類
class Map:
    def __init__(self):
        self.grid = [[TileType.EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.generate_map()
        self.shrink_count = 0  # 縮小次數
        self.timer = SHRINK_COUNT  # 縮小地圖的倒計時 60 秒（30 幀/秒）
        self.is_finished = False

    def generate_map(self):
        # 邊緣設置為不可破壞磚塊
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if (x == 0 or x == GRID_SIZE - 1) and y != GRID_SIZE - 1:
                    self.grid[x][y] = TileType.AROUND
                elif y == 0 or y == GRID_SIZE - 1:
                    self.grid[x][y] = TileType.UNBREAKABLE
                # 設置偶數坐標為不可破壞磚塊
                elif x % 2 == 0 and y % 2 == 0 and not (x == GRID_SIZE-2 and y == GRID_SIZE-2):
                    self.grid[x][y] = TileType.UNBREAKABLE
                else:
                    # 隨機生成草堆，并 x = y 軸對稱
                    if random.random() < 0.2 and not (x == 1 and y == 1) and not (x == GRID_SIZE-2 and y == GRID_SIZE-2):
                        self.grid[x][y] = TileType.BREAKABLE
                        self.grid[GRID_SIZE - 1 - x][GRID_SIZE - 1 - y] = TileType.BREAKABLE

       # player1 周圍沒有炸彈
        for y in range(1, 3):
            for x in range(1, 3):
                if self.grid[x][y] == TileType.BREAKABLE:
                    self.grid[x][y] = TileType.EMPTY
 
        # player2 周圍沒有炸彈
        for y in range(GRID_SIZE - 3, GRID_SIZE - 1):
            for x in range(GRID_SIZE - 3, GRID_SIZE - 1):
                if self.grid[x][y] == TileType.BREAKABLE:
                    self.grid[x][y] = TileType.EMPTY

        # 隨機生成 BUFF
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

    # 縮小地圖
    def shrink_map(self):
        if self.timer > 0:
            self.timer -= 1
        
        # 剛好能縮到地圖中心
        elif self.timer == 0 and GRID_SIZE // 2 + 1 > self.shrink_count:
            layer = self.shrink_count
            for i in range(layer, GRID_SIZE - layer):
                self.grid[layer][i] = TileType.UNBREAKABLE
                self.grid[GRID_SIZE - 1 - layer][i] = TileType.UNBREAKABLE
                self.grid[i][layer] = TileType.UNBREAKABLE
                self.grid[i][GRID_SIZE - 1 - layer] = TileType.UNBREAKABLE
            self.shrink_count += 1
            self.timer = SHRINK_COUNT  # 重設倒計時
        elif GRID_SIZE // 2 + 1 <= self.shrink_count:
            self.is_finished = True

    # 繪製地圖
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