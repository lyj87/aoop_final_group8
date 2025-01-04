from constant import *

# 玩家类
class Player:
    def __init__(self, x, y, frames, explosion_range, score, heal, bomb_num, plant_num, name):
        self.dx = x
        self.dy = y
        self.x = x * TILE_SIZE  # 轉換成像素坐標
        self.y = y * TILE_SIZE  # 轉換成像素坐標
        self.speed = 4  # 每幀移動的像素數
        self.direction = "DOWN"  # 初始方向
        self.image = frames
        self.frame_index = 0  # 當前帧
        self.frame_timer = 0  # 帧计时器，用于调整動畫速度
        self.image_frame = frames  # 
        self.placed_bomb = 0  # 是否正在放置炸彈
        self.placed_water = 0  # 是否正在放置植物
        self.name = name

        self.explosion_range = explosion_range  # 初始爆炸範圍
        self.score = score  # 初始分數為
        self.heal = heal    # 初始生命值
        self.bomb_num = bomb_num    # 初始炸彈數量
        self.plant_num = plant_num  # 初始植物數量

    def set_direction(self, dx, dy):
        if dx > 0:
            self.direction = "RIGHT"
        elif dx < 0:
            self.direction = "LEFT"
        elif dy > 0:
            self.direction = "DOWN"
        elif dy < 0:
            self.direction = "UP"

    # 移動
    def move(self, dx, dy, grid):
        self.set_direction(dx, dy)
        # 確保不會超出邊界
        new_x = max(1, GRID_SIZE - 1, self.x + dx * self.speed)
        new_y = max(1, GRID_SIZE - 1, self.y + dy * self.speed)
        # new_x = self.x + dx * self.speed
        # new_y = self.y + dy * self.speed
        if self.check_collision(new_x, new_y, grid) and (dy != 0 or dx != 0):
            self.x = new_x
            self.y = new_y
            return (self.x, self.y)  # 未碰撞，成功移動
        return False  # 碰撞

    def check_collision(self, new_x, new_y, grid):
        # 角色四個角的坐標（像素）
        corners = [
            (new_x + 8 , new_y + 8), # 左上角
            (new_x + TILE_SIZE - 1 - 8 , new_y + 8), # 右上角
            (new_x + 8, new_y + TILE_SIZE - 1 - 8), # 左下角
            (new_x + TILE_SIZE - 1 - 8, new_y + TILE_SIZE - 1 - 8), # 右下角
        ]

        for corner in corners:
            x = corner[0] // TILE_SIZE
            y = corner[1] // TILE_SIZE
            # 確保不會超出邊界
            if (x + 1 < GRID_SIZE and x - 1 > 0 and y + 1 < GRID_SIZE and y - 1 > 0):
                if (grid[x + 1][y] == TileType.UNBREAKABLE and grid[x - 1][y] == TileType.UNBREAKABLE and
                    grid[x][y + 1] == TileType.UNBREAKABLE and grid[x][y - 1] == TileType.UNBREAKABLE):
                    self.heal = 0 
            # 碰撞檢測
            if (grid[x][y] == TileType.BREAKABLE or grid[x][y] == TileType.UNBREAKABLE or grid[x][y] == TileType.AROUND or 
                grid[x][y] == TileType.GRASS_BUFF_NUM or grid[x][y] == TileType.GRASS_BUFF_RANGE or grid[x][y] == TileType.GRASS_HEAL):
                return False
            # 炸彈數量+1
            if (grid[x][y] == TileType.BUFF_NUM):
                self.bomb_num += 1
                grid[x][y] = TileType.EMPTY
            # 爆炸範圍+1
            if (grid[x][y] == TileType.BUFF_RANGE):
                self.explosion_range += 1
                grid[x][y] = TileType.EMPTY
            # 生命值+1
            if (grid[x][y] == TileType.HEAL):
                self.heal += 1
                grid[x][y] = TileType.EMPTY
            
            # 當角色 placed_water == 1 (放置炸彈后)，四個角都離開炸彈格，placed_water = 0
            if (grid[corners[0][0] // TILE_SIZE][corners[0][1] // TILE_SIZE] != TileType.BOMB and 
                grid[corners[1][0] // TILE_SIZE][corners[1][1] // TILE_SIZE] != TileType.BOMB and
                grid[corners[2][0] // TILE_SIZE][corners[2][1] // TILE_SIZE] != TileType.BOMB and 
                grid[corners[3][0] // TILE_SIZE][corners[3][1] // TILE_SIZE] != TileType.BOMB and 
                self.placed_bomb == 1):
                self.placed_bomb = 0
            # 當角色 placed_water == 0 (未放置炸彈)，其中一個角都進入炸彈格，角色無法前進
            if (grid[x][y] == TileType.BOMB and self.placed_bomb == 0):
                return False
            
            # 當角色 placed_water == 1 (放置炸彈后)，四個角都離開炸彈格，placed_water = 0
            if (grid[corners[0][0] // TILE_SIZE][corners[0][1] // TILE_SIZE] != TileType.WATER and 
                grid[corners[1][0] // TILE_SIZE][corners[1][1] // TILE_SIZE] != TileType.WATER and
                grid[corners[2][0] // TILE_SIZE][corners[2][1] // TILE_SIZE] != TileType.WATER and 
                grid[corners[3][0] // TILE_SIZE][corners[3][1] // TILE_SIZE] != TileType.WATER and 
                self.placed_water == 1):
                self.placed_water = 0
            # 當角色 placed_water == 0 (未放置炸彈)，其中一個角都進入炸彈格，角色無法前進
            if (grid[x][y] == TileType.WATER and self.placed_water == 0):
                return False
        return True
    
    # 更新幀
    def update_animation(self):
        self.frame_timer += 1
        if self.frame_timer >= 6:  # 6 幀切換一次
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.image_frame[self.direction])
    
    def draw(self, screen):
        # 繪製當前方向和幀
        current_frame = self.image_frame[self.direction][self.frame_index]
        screen.blit(current_frame, (self.x, self.y))

    # 繪製角色受傷
    def damage_draw(self, screen):
        current_frame = damage_player_frames[self.direction][self.frame_index]
        screen.blit(current_frame, (self.x, self.y))