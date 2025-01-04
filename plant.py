from constant import *

class Plant:
    def __init__(self, x, y):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.tile_x = x
        self.tile_y = y
        self.timer = 150  # 成長倒計時 5 秒（30 幀/秒）
        self.grown = False

    def update(self, grid):
        if self.timer > 0:
            grid[self.tile_x][self.tile_y] = TileType.WATER  # 標記水的位置
            self.timer -= 1
        # 成長
        elif not self.grown:
            self.grown = True
            grid[self.tile_x][self.tile_y] = TileType.BREAKABLE  # 成長後變成草叢

    def draw(self, screen):
        if self.timer > 0:
            # 繪製水
            screen.blit(tile_water_img, (self.x, self.y))

    def is_finished(self):
        return self.grown
