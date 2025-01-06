import pygame
from constant import *

import pygame

class Scoreboard:
    def __init__(self, players, map):
        self.players = players  # 保存传入的玩家列表
        self.font = pygame.font.SysFont("Arial", 18)
        self.subtitle_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.map = map

    def draw(self, screen):
        # 繪製分數板背景
        pygame.draw.rect(screen, (128, 128, 128), (GRID_SIZE * TILE_SIZE, 0, SCOREBOARD_WIDTH, GRID_SIZE * TILE_SIZE))

        # 暫停
        puase_text = self.subtitle_font.render("Press 'P' to Pause", True, WHITE)
        screen.blit(puase_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - puase_text.get_width() // 2, 40))

        timer_text = self.subtitle_font.render(f"TIMER : {int(self.map.timer/30) + 1}", True, WHITE)
        screen.blit(timer_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - timer_text.get_width() // 2, 70))
        instructions = [
                ["WASD to move", "F to place bomb", "G to place plant"],
                ["Arrow keys to move", "M to place bomb", "N to place plant"]
            ]
        
        # 玩家信息
        y_offset = 120  # 初始Y位置
        for player in self.players:
            # 名称
            name_text = self.subtitle_font.render(player.name, True, WHITE)
            screen.blit(name_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - name_text.get_width() // 2, y_offset))

            # 分數
            score_text = self.font.render(f"Score :  {player.score}", True, WHITE)
            screen.blit(score_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - score_text.get_width() // 2, y_offset + 35))

            # 生命值
            heal_text = self.font.render(f"Heal   :  {player.heal}", True, WHITE)
            screen.blit(heal_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - heal_text.get_width() // 2, y_offset + 60))

            # 炸彈數量
            bomb_text = self.font.render(f"Bomb  :  {player.bomb_num}", True, WHITE)
            screen.blit(bomb_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - bomb_text.get_width() // 2, y_offset + 85))

            # 爆炸範圍
            explosion_text = self.font.render(f"Range :  {player.explosion_range}", True, WHITE)
            screen.blit(explosion_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - explosion_text.get_width() // 2, y_offset + 110))

            # 下一個玩家信息的Y偏移量
            y_offset += 135

            # 操作说明
            for instruction in instructions[self.players.index(player)]:
                instruction_text = self.font.render(instruction, True, WHITE)
                screen.blit(instruction_text, (GAME_WIDTH + SCOREBOARD_WIDTH // 2 - instruction_text.get_width() // 2, y_offset))
                y_offset += 20  # 每条指令之间的垂直间距
            y_offset += 30  # 在玩家信息之后增加一些垂直间距
