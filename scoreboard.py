import pygame
from constant import GRID_SIZE, TILE_SIZE, SCOREBOARD_WIDTH, GRAY, WHITE

class Scoreboard:
    def __init__(self, player):
        self.player = player
        self.font = pygame.font.SysFont("Arial", 24)

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, (GRID_SIZE * TILE_SIZE, 0, SCOREBOARD_WIDTH, GRID_SIZE * TILE_SIZE))
        title_text = self.font.render("PAUSE", True, WHITE)
        screen.blit(title_text, (GRID_SIZE * TILE_SIZE + 20, 40))
        score_text = self.font.render(f"player1", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 120))
        score_text = self.font.render(f"score: {self.player.score}", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 160))
        score_text = self.font.render(f"heal : {self.player.heal}", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 190))
        score_text = self.font.render(f"bomb : {self.player.bomb}", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 220))