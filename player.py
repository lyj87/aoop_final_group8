from constant import *

# 玩家类
class Player:
    def __init__(self, x, y, frames, explosion_range, score, heal, bomb_num):
        self.dx = x
        self.dy = y
        self.x = x * TILE_SIZE  # 转换为像素坐标
        self.y = y * TILE_SIZE
        self.speed = 4  # 每帧移动的像素距离
        self.direction = "DOWN"  # 初始方向为向下
        self.image = frames
        self.frame_index = 0  # 当前帧索引
        self.frame_timer = 0  # 用于控制动画速度
        self.image_frame = frames  # 所有方向的帧
        self.placed_bomb = 0  # 用于记录最近一次放置炸弹的位置
        self.placed_water = 0  # 用于记录最近一次放置炸弹的位置

        self.explosion_range = explosion_range  # 初始爆炸范围为 1 格
        self.score = score
        self.heal = heal
        self.bomb_num = bomb_num

    def set_direction(self, dx, dy):
        if dx > 0:
            self.direction = "RIGHT"
        elif dx < 0:
            self.direction = "LEFT"
        elif dy > 0:
            self.direction = "DOWN"
        elif dy < 0:
            self.direction = "UP"

    def move(self, dx, dy, grid):
        # 更新方向
        self.set_direction(dx, dy)
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        if self.check_collision(new_x, new_y, grid) and (dy != 0 or dx != 0):
            self.x = new_x
            self.y = new_y

    def check_collision(self, new_x, new_y, grid):
        # 角色四个角的像素坐标
        corners = [
            (new_x + 8 , new_y + 8), # 左上角
            (new_x + TILE_SIZE - 1 - 8 , new_y + 8), # 右上角
            (new_x + 8, new_y + TILE_SIZE - 1 - 8), # 左下角
            (new_x + TILE_SIZE - 1 - 8, new_y + TILE_SIZE - 1 - 8), # 右下角
        ]

        for corner in corners:
            x = corner[0] // TILE_SIZE
            y = corner[1] // TILE_SIZE 
            if (grid[x][y] == TileType.BREAKABLE or grid[x][y] == TileType.UNBREAKABLE or grid[x][y] == TileType.AROUND or 
                grid[x][y] == TileType.GRASS_BUFF_NUM or grid[x][y] == TileType.GRASS_BUFF_RANGE or grid[x][y] == TileType.GRASS_HEAL):
                return False
            if (grid[x][y] == TileType.BUFF_NUM):
                self.bomb += 1
                grid[x][y] = TileType.EMPTY
            if (grid[x][y] == TileType.BUFF_RANGE):
                self.explosion_range += 1
                grid[x][y] = TileType.EMPTY
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
    
    def update_animation(self):
        # 每隔一定时间更新动画帧
        self.frame_timer += 1
        if self.frame_timer >= 6:  # 6帧更新一次
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.image_frame[self.direction])
    
    def draw(self, screen):
        # 获取当前方向和帧
        current_frame = self.image_frame[self.direction][self.frame_index]
        screen.blit(current_frame, (self.x, self.y))

    def damage_draw(self, screen):
        current_frame = damage_player_frames[self.direction][self.frame_index]
        screen.blit(current_frame, (self.x, self.y))