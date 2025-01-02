import pygame
from constant import *

import pygame

class Scoreboard:
    def __init__(self, players):
        self.players = players  # 保存传入的玩家列表
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, screen):
        # 绘制背景
        pygame.draw.rect(screen, (128, 128, 128), (GRID_SIZE * TILE_SIZE, 0, SCOREBOARD_WIDTH, GRID_SIZE * TILE_SIZE))

        # 标题
        title_text = self.font.render("PAUSE", True, (255, 255, 255))
        screen.blit(title_text, (GRID_SIZE * TILE_SIZE + 20, 40))

        # 遍历玩家，显示数据
        y_offset = 100  # 初始Y位置
        for player in self.players:
            # 玩家名称
            # name_text = self.font.render(player.name, True, (255, 255, 255))
            # screen.blit(name_text, (GRID_SIZE * TILE_SIZE + 20, y_offset))

            # 分数
            score_text = self.font.render(f"Score: {player.score}", True, (255, 255, 255))
            screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, y_offset + 40))

            # 生命值
            heal_text = self.font.render(f"Heal: {player.heal}", True, (255, 255, 255))
            screen.blit(heal_text, (GRID_SIZE * TILE_SIZE + 20, y_offset + 70))

            # 炸弹
            bomb_text = self.font.render(f"Bomb: {player.bomb_num}", True, (255, 255, 255))
            screen.blit(bomb_text, (GRID_SIZE * TILE_SIZE + 20, y_offset + 100))

            # 炸弹
            bomb_text = self.font.render(f"Range: {player.explosion_range}", True, (255, 255, 255))
            screen.blit(bomb_text, (GRID_SIZE * TILE_SIZE + 20, y_offset + 130))

            # 下一个玩家的Y偏移
            y_offset += 150