import pygame
from constant import *

import pygame

class Scoreboard:
    def __init__(self, players, map):
        self.players = players  # 保存传入的玩家列表
        self.font = pygame.font.SysFont("Arial", 24)
        self.map = map

    def draw(self, screen):
        # 繪製分數板背景
        pygame.draw.rect(screen, (128, 128, 128), (GRID_SIZE * TILE_SIZE, 0, SCOREBOARD_WIDTH, GRID_SIZE * TILE_SIZE))

        # 暫停
        puase_text = self.font.render("double press 'P' goto start page", True, WHITE)
        screen.blit(puase_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - puase_text.get_width() // 2, 40))

        timer_text = self.font.render(f"TIMER : {int(self.map.timer/30) + 1}", True, WHITE)
        screen.blit(timer_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - timer_text.get_width() // 2, 70))

        # 玩家信息
        y_offset = 120  # 初始Y位置
        for player in self.players:
            # 名称
            name_text = self.font.render(player.name, True, WHITE)
            screen.blit(name_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - name_text.get_width() // 2, y_offset))

            # 分數
            score_text = self.font.render(f"Score :  {player.score}", True, WHITE)
            screen.blit(score_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - score_text.get_width() // 2, y_offset + 30))

            # 生命值
            heal_text = self.font.render(f"Heal   :  {player.heal}", True, WHITE)
            screen.blit(heal_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - heal_text.get_width() // 2, y_offset + 60))

            # 炸彈數量
            bomb_text = self.font.render(f"Bomb  :  {player.bomb_num}", True, WHITE)
            screen.blit(bomb_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - bomb_text.get_width() // 2, y_offset + 90))

            # 爆炸範圍
            explosion_text = self.font.render(f"Range :  {player.explosion_range}", True, WHITE)
            screen.blit(explosion_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - explosion_text.get_width() // 2, y_offset + 120))

            # 下一個玩家信息的Y偏移量
            y_offset += 170