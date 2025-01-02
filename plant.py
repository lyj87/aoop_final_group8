from constant import *

class Plant:
    def __init__(self, x, y):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.tile_x = x
        self.tile_y = y
        self.timer = 150  # 成长倒计时 5 秒（30 帧/秒）
        self.grown = False

    def update(self, grid):
        if self.timer > 0:
            grid[self.tile_x][self.tile_y] = TileType.WATER  # 标记种子位置
            self.timer -= 1
        elif not self.grown:
            self.grown = True
            grid[self.tile_x][self.tile_y] = TileType.BREAKABLE  # 变成草丛

    def draw(self, screen):
        if self.timer > 0:
            # 绘制种子
            screen.blit(tile_water_img, (self.x, self.y))
