import pygame
from constant import GRID_SIZE, TILE_SIZE, SCOREBOARD_WIDTH, GRAY, WHITE, SCREEN_HEIGHT

class Scoreboard:
    def __init__(self, players):
        self.players = players
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 24, bold=True)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, (GRID_SIZE * TILE_SIZE, 0, SCOREBOARD_WIDTH, SCREEN_HEIGHT))
        title_text = self.font.render("PAUSE", True, WHITE)
        screen.blit(title_text, (GRID_SIZE * TILE_SIZE + 20, 20))

        # 繪製標題
        title_text = self.title_font.render("Scoreboard", True, WHITE)
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
            bomb_text = self.font.render(f"Bomb: {player.bomb}", True, (255, 255, 255))
            screen.blit(bomb_text, (GRID_SIZE * TILE_SIZE + 20, y_offset + 100))

            # 下一个玩家的Y偏移
            y_offset += 150
        # 繪製菜單
        menu_text = self.title_font.render("Menu", True, WHITE)
        screen.blit(menu_text, (GRID_SIZE * TILE_SIZE + 20, y_offset))

        # 菜單選項
        menu_items = ["Player 1","WASD: Move","Q: Place Bomb","","Player 2","Arrow Keys: Move", "Shift: Place Bomb","","ESC: Quit"]
        for i, item in enumerate(menu_items):
            item_text = self.font.render(item, True, WHITE)
            screen.blit(item_text, (GRID_SIZE * TILE_SIZE + 20, y_offset + i * 30))