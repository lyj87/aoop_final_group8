import pygame
import sys
from constant import *


class GameOverScreen:
    def __init__(self, screen, player1, player2):
        self.screen = screen
        self.player1 = player1
        self.player2 = player2
        self.state = "gameover"
        self.font = pygame.font.SysFont('Arial', 25)
        self.title_font = pygame.font.SysFont('Arial', 80)

    def display(self):
        clock = pygame.time.Clock()
        while self.state == "gameover":
            # screen.fill((BLACK))

            # 判斷贏家並顯示文字
            if self.player1.heal <= 0 and self.player2.heal > 0:
                winner_text = self.title_font.render(f"{self.player2.name} Wins!", True, WHITE)
            elif self.player2.heal <= 0 and self.player1.heal > 0:
                winner_text = self.title_font.render(f"{self.player1.name} Wins!", True, WHITE)
            else:
                winner_text = self.title_font.render("BOTH DEATH !!!", True, WHITE)
            self.screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 - winner_text.get_height() // 2 - 50))

            # 顯示 Game Over
            game_over_text = self.title_font.render("Game Over", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height() // 2))

            # 顯示 restart 提示
            retry_text = self.font.render("Press 'R' to Restart", True, WHITE)
            self.screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 200))

            # 顯示 goto Start Page 提示
            start_text = self.font.render("Press 'P' goto Start Page", True, WHITE)
            self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 230))
            
            # 顯示 exit 提示
            exit_text = self.font.render("Press any key to Exit", True, WHITE)
            self.screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 260))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.state = "game"
                        print("replay game")
                        pygame.time.wait(150)
                    elif event.key == pygame.K_p:
                        self.state = "start"
                        print("goto start screen")
                        pygame.time.wait(150)
                    else:
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            clock.tick(30)



if __name__ == "__main__":
    from player import Player
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(BLACK)
    player1 = Player(1, 1, player1_frames, explosion_range = 1, score = 0, heal = 0, bomb_num = 1, plant_num = 1, name = "player1")
    player2 = Player(GRID_SIZE - 2 , GRID_SIZE - 2, player2_frames, explosion_range = 1, score = 0, heal = 2, bomb_num = 1, plant_num = 1, name = "player2")
    state = "gameover"
    overscreen = GameOverScreen(screen, player1, player2)
    overscreen.display()