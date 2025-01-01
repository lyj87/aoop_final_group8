import pygame
from constant import GRID_SIZE, TILE_SIZE, SCOREBOARD_WIDTH, GRAY, WHITE, SCREEN_HEIGHT

class Scoreboard:
    def __init__(self, player, player2):
        self.player = player
        self.player2 = player2
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

        # 繪製player1分數、爆炸範圍
        text = self.subtitle_font.render(f"Player 1", True, WHITE)
        screen.blit(text, (GRID_SIZE * TILE_SIZE + 20, 70))
    
        score_text = self.font.render(f"Score: {self.player.score}", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 100))

        explosion_range_text = self.font.render(f"Explosion Range: {self.player.explosion_range}", True, WHITE)
        screen.blit(explosion_range_text, (GRID_SIZE * TILE_SIZE + 20, 130))

        score_text = self.font.render(f"score: {self.player.score}", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 160))
        score_text = self.font.render(f"heal : {self.player.heal}", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 190))
        score_text = self.font.render(f"bomb : {self.player.bomb}", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 220))

        # 繪製player2分數、爆炸範圍
        text2 = self.subtitle_font.render(f"Player 2", True, WHITE)
        screen.blit(text2, (GRID_SIZE * TILE_SIZE + 20, 270))

        score_text2 = self.font.render(f"Score: {self.player2.score}", True, WHITE)
        screen.blit(score_text2, (GRID_SIZE * TILE_SIZE + 20, 300))

        explosion_range_text = self.font.render(f"Explosion Range: {self.player.explosion_range}", True, WHITE)
        screen.blit(explosion_range_text, (GRID_SIZE * TILE_SIZE + 20, 330))

        score_text = self.font.render(f"score: {self.player.score}", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 360))
        score_text = self.font.render(f"heal : {self.player.heal}", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 390))
        score_text = self.font.render(f"bomb : {self.player.bomb}", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 420))

        # 繪製菜單
        menu_text = self.title_font.render("Menu", True, WHITE)
        screen.blit(menu_text, (GRID_SIZE * TILE_SIZE + 20, 470))

        # 菜單選項
        menu_items = ["Player 1","WASD: Move","Q: Place Bomb","","Player 2","Arrow Keys: Move", "Shift: Place Bomb","","ESC: Quit"]
        for i, item in enumerate(menu_items):
            item_text = self.font.render(item, True, WHITE)
            screen.blit(item_text, (GRID_SIZE * TILE_SIZE + 20, 500 + i * 30))
