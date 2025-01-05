import sys
import keyboard
import pygame
from constant import *
from game import Game
from page_start import MainMenu
from page_gameover import GameOverScreen

pygame.init()
font = pygame.font.SysFont('Arial', 32)
title_font = pygame.font.SysFont('notosanscjktc', 84)
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

if __name__ == "__main__": 
    # 当前状态：start, game, gameover, pause
    state = "start"
    while running:
        if state == "start":
            mainmenu = MainMenu()
            name1, name2 = mainmenu.start(screen, font, title_font)
            state = mainmenu.state
            print('player1:', name1, ', player2:', name2)
            print("state:", state)        
        elif state == "game":
            game = Game(screen, name1, name2)
            game.game_loop()
            state = game.state
        elif state == "gameover":
            state = "gameover"
            overscreen = GameOverScreen(screen, game.player1, game.player2)
            overscreen.display()
        elif state == "pause":
            game.pause_screen()
            state = game.state
        check_quit()