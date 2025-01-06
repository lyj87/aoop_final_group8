import sys
import keyboard
import pygame
from constant import *
from game import Game
from page_start import MainMenu
from page_gameover import GameOverScreen

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
running = True

def check_quit():
    # 按 esc 退出遊戲
    if keyboard.is_pressed('esc'):
        running = False
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()


state = "start"
while running:
    if state == "start":
        mainmenu = MainMenu(screen)
        name1, name2 = mainmenu.start()
        state = mainmenu.state
        print('player1:', name1, ', player2:', name2)
        print("state:", state)        
    elif state == "game":
        game = Game(screen, name1, name2)
        print(state)
        game.game_loop()
        state = game.state
    elif state == "gameover":
        state = "gameover"
        overscreen = GameOverScreen(screen)
        overscreen.display()
    elif state == "pause":
        game.pause_screen()
        state = game.state
    check_quit()