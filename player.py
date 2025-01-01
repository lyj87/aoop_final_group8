import pygame
import random
import keyboard

from constant import TILE_SIZE, TileType

player_img = pygame.image.load("./assets/player.png")
player_frames = {
    "DOWN": [],
    "RIGHT": [],
    "LEFT": [],
    "UP": []
}
for i in range(6):  # 6 frames per direction
    player_frames["DOWN"].append(player_img.subsurface((i * 32, 3 * 32, 32, 32)))
    player_frames["RIGHT"].append(player_img.subsurface((i * 32, 4 * 32, 32, 32)))
    player_frames["LEFT"].append(player_img.subsurface((i * 32, 4 * 32, 32, 32)))
    player_frames["UP"].append(player_img.subsurface((i * 32, 5 * 32, 32, 32)))

# 玩家类
class Player:
    def __init__(self, x, y, frames):
        self.dx = x
        self.dy = y
        self.x = x * TILE_SIZE  # 转换为像素坐标
        self.y = y * TILE_SIZE
        self.speed = 4  # 每帧移动的像素距离
        self.direction = "DOWN"  # 初始方向为向下
        
        self.frame_index = 0  # 当前帧索引
        self.frame_timer = 0  # 用于控制动画速度
        self.image_frame = frames  # 所有方向的帧

        self.explosion_range = 1  # 初始爆炸范围为 1 格
        self.score = 0
        self.heal = 3
        self.bomb = 3

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
            if (grid[x][y] != TileType.EMPTY):  # 如果角点处是障碍物
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