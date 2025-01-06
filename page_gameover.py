import pygame
import sys
from constant import *
from page import Page

class GameOverScreen(Page):
    def __init__(self, screen):
        super().__init__(screen)  # Call the parent class (Page) constructor
        self.font = pygame.font.SysFont('Arial', 25)
        self.title_font = pygame.font.SysFont('Arial', 80)
        self.state = "gameover"
    def display(self, player1, player2):
        clock = pygame.time.Clock()
        
        while self.state == "gameover":
            #self.screen.fill(BLACK)

            # Determine the winner and display text
            if player1.heal <= 0 and player2.heal > 0:
                winner_text = self.title_font.render(f"{player2.name} Wins!", True, WHITE)
            elif player2.heal <= 0 and player1.heal > 0:
                winner_text = self.title_font.render(f"{player1.name} Wins!", True, WHITE)
            else:
                winner_text = self.title_font.render("BOTH DEATH !!!", True, WHITE)
            self.screen.blit(winner_text, (SCREEN_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 - winner_text.get_height() // 2 - 50))

            # Display Game Over
            game_over_text = self.title_font.render("Game Over", True, WHITE)
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height() // 2))

            # Display restart prompt
            retry_text = self.font.render("Press 'R' to Restart", True, WHITE)
            self.screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 200))

            # Display go to Start Page prompt
            start_text = self.font.render("Press 'P' to go to Start Page", True, WHITE)
            self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 230))
            
            # Display exit prompt
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
                        print("go to start screen")
                        pygame.time.wait(150)
                    else:
                        pygame.quit()
                        sys.exit()

            pygame.display.flip()
            clock.tick(30)

# if __name__ == "__main__":
#     from player import Player
#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     screen.fill(BLACK)
#     player1 = Player(1, 1, "player 1", player1_frames)
#     player2 = Player(GRID_SIZE- 2 , GRID_SIZE - 2, "player 2",player2_frames)
#     overscreen = GameOverScreen(screen)
#     overscreen.display(player1, player2)