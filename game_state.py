import pygame
import keyboard
import sys

from constant import *
from player import Player
from map import Map
from bomb import Bomb
from scoreboard import Scoreboard
from plant import Plant

# 初始化 Pygame
pygame.init()

# 字體
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 84)
puase_font = pygame.font.Font(None, 300)

global bombs_list
global plant_list

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"{GRID_SIZE}x{GRID_SIZE} Map Game")
        self.clock = pygame.time.Clock()

        # 遊戲狀態
        self.running = True
        self.state = "start"  # 当前状态：start, game, gameover

        # 玩家對象
        self.player1 = Player(1, 1, player1_frames, explosion_range = 1, score = 0, heal = 2, bomb_num = 1, plant_num = 1, name = "")
        self.player2 = Player(GRID_SIZE - 2 , GRID_SIZE - 2, player2_frames, explosion_range = 1, score = 0, heal = 2, bomb_num = 1, plant_num = 1, name = "")
        self.game_map = Map()
        self.scoreboard = Scoreboard([self.player1, self.player2], self.game_map)

        self.change_name = 1  # 1 for player1_name, 2 for player2_name
        self.p_count = 0  # 按下 P 鍵的次數

    def reset(self):
        self.player1 = Player(1, 1, player1_frames, explosion_range = 1, score = 0, heal = 2, bomb_num = 1, plant_num = 1, name = self.player1.name)
        self.player2 = Player(GRID_SIZE - 2 , GRID_SIZE - 2, player2_frames, explosion_range = 1, score = 0, heal = 2, bomb_num = 1,  plant_num = 1, name = self.player2.name)
        self.game_map = Map()
        self.scoreboard = Scoreboard([self.player1, self.player2], self.game_map)
        self.p_count = 0
        self.change_name = 1


    def start_screen(self):
        while self.state == "start":
            # 重置 p_count
            self.p_count = 0
            # self.screen.fill(WHITE)
            self.screen.blit(start_img, (0, 0))

            # 標題
            title_text = title_font.render("BomberMan", True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

            # player1 name 输入框
            player1_text = font.render("player1:", True, WHITE)
            self.screen.blit(player1_text, (SCREEN_WIDTH // 2 - player1_text.get_width() // 2 - 100, SCREEN_HEIGHT // 2 - 80))
            input_box1 = pygame.Rect(SCREEN_WIDTH // 2 - player1_text.get_width() // 2, SCREEN_HEIGHT // 2  - 84, 200, 34)
            pygame.draw.rect(self.screen, GRAY, input_box1, 2)
            text_surface1 = font.render(self.player1.name, True, WHITE)
            self.screen.blit(text_surface1, (input_box1.x + 5, input_box1.y + 5))

            # player2 name 輸入框
            player2_text = font.render("player2:", True, WHITE)
            self.screen.blit(player2_text, (SCREEN_WIDTH // 2 - player2_text.get_width() // 2 - 100, SCREEN_HEIGHT // 2 - 30))
            input_box2 = pygame.Rect(SCREEN_WIDTH // 2 - player2_text.get_width() // 2, SCREEN_HEIGHT // 2 - 34, 200, 34)
            pygame.draw.rect(self.screen, GRAY, input_box2, 2)
            text_surface2 = font.render(self.player2.name, True, WHITE)
            self.screen.blit(text_surface2, (input_box2.x + 5, input_box2.y + 5))

            # 開始按鈕
            # start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, 290, 200, 50)
            # pygame.draw.rect(self.screen, BLUE, start_button)
            # button_text = font.render("START GAME", True, WHITE)
            # self.screen.blit(button_text, (start_button.x + (start_button.width - button_text.get_width()) // 2,
            #                                start_button.y + (start_button.height - button_text.get_height()) // 2))
            
            # 顯示 enter 提示
            enter_text = font.render("Press ENTER to Restart", True, WHITE)
            self.screen.blit(enter_text, (SCREEN_WIDTH // 2 - enter_text.get_width() // 2, SCREEN_HEIGHT // 2 + 200))

            # 顯示 tab 提示
            tab_text = font.render("Press TAB to Change Input Box", True, WHITE)
            self.screen.blit(tab_text, (SCREEN_WIDTH // 2 - tab_text.get_width() // 2, SCREEN_HEIGHT // 2 + 230))

            # start 按鈕點擊事件
            # for event in pygame.event.get():
            #     print(event)
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         print(f"Mouse clicked at {event.pos}")
            #         if start_button.collidepoint(event.pos):
            #             print("Start button clicked")
            #             if self.player1.name.strip() and self.player2.name.strip():
            #                 if not self.player1.name.strip():
            #                     print("player1 name are empty")
            #                 if not self.player2.name.strip():
            #                     print("player2 name are empty")
            #                 self.state = "game"     # 切換到遊戲狀態
            #             else:
            #                 print("player1 and player2 name are empty")

            pygame.display.flip()

            # 檢測該誰輸入
            if self.change_name == 1:
                self.handle_input("player1")
            elif self.change_name == 2:
                self.handle_input("player2")

            # 切換輸入框
            if keyboard.is_pressed("tab"):
                self.change_name = 2 if self.change_name == 1 else 1
                pygame.time.wait(150)

            # enter 進入遊戲
            if keyboard.is_pressed("enter"):
                if self.player1.name.strip() and self.player2.name.strip():
                    print(f"player: {self.player1.name}")
                    print(f"player: {self.player2.name}")
                    self.state = "game"     # 切換到遊戲狀態
                elif not self.player1.name.strip():
                        print("player1 name is empty")
                elif not self.player2.name.strip():
                        print("player2 name is empty")
                else:
                    print("player1 and player2 name are empty")
                pygame.time.wait(150)

            self.check_quit()

    def game_loop(self):
        bombs_list = [] # 炸彈列表
        plant_list = [] # 植物列表
        while self.state == "game":
            # 繪製地圖
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    self.screen.blit(background_img, (x * TILE_SIZE, y * TILE_SIZE))

            # player1 移動
            dx, dy = 0, 0
            if keyboard.is_pressed('w'):
                dy = -1
            if keyboard.is_pressed('s'):
                dy = 1
            if keyboard.is_pressed('a'):
                dx = -1
            if keyboard.is_pressed('d'):
                dx = 1
            self.player1.move(dx, dy, self.game_map.grid)

            # player2 移動
            dx2, dy2 = 0, 0
            if keyboard.is_pressed('up'):
                dy2 = -1
            if keyboard.is_pressed('down'):
                dy2 = 1
            if keyboard.is_pressed('left'):
                dx2 = -1
            if keyboard.is_pressed('right'):
                dx2 = 1
            self.player2.move(dx2, dy2, self.game_map.grid)

            # player 1 放置炸彈
            if keyboard.is_pressed('q'):
                # +8是爲了補償player.cheak_collision的偏移
                player_tile_x = (self.player1.x + 8) // TILE_SIZE
                player_tile_y = (self.player1.y + 8) // TILE_SIZE
                if len(bombs_list) < self.player1.bomb_num and not any(bomb.tile_x == player_tile_x and bomb.tile_y == player_tile_y for bomb in bombs_list):
                    bombs_list.append(Bomb(player_tile_x, player_tile_y, self.player1.explosion_range, self.player1))
                    self.player1.placed_bomb = 1

            # player 1 放置植物
            if keyboard.is_pressed('e'):
                # +8是爲了補償player.cheak_collision的偏移
                player_tile_x = (self.player1.x + 8) // TILE_SIZE
                player_tile_y = (self.player1.y + 8) // TILE_SIZE
                if len(plant_list) < self.player1.plant_num and not any(plant.tile_x == player_tile_x and plant.tile_y == player_tile_y for plant in plant_list):
                    plant_list.append(Plant(player_tile_x, player_tile_y))
                    self.player1.placed_water = 1

            # if keyboard.is_pressed('t') and not key_pressed:
            #     key_pressed = True  # 设置为已触发
            #     self.player1.explosion_range += 1
            # elif not keyboard.is_pressed('e'):
            #     key_pressed = False  # 当按键松开时，重置状态

            # player 2 放置炸彈
            if keyboard.is_pressed('shift'):
                player2_tile_x = (self.player2.x + 8) // TILE_SIZE
                player2_tile_y = (self.player2.y + 8) // TILE_SIZE
                if len(bombs_list) < self.player2.bomb_num and not any(bomb.tile_x == player2_tile_x and bomb.tile_y == player2_tile_y for bomb in bombs_list):
                    bombs_list.append(Bomb(player2_tile_x, player2_tile_y, self.player2.explosion_range, self.player2))
                    self.player2.placed_bomb = 1

            if keyboard.is_pressed('/'):
                # +8是爲了補償player.cheak_collision的偏移
                player_tile_x = (self.player2.x + 8) // TILE_SIZE
                player_tile_y = (self.player2.y + 8) // TILE_SIZE
                if len(plant_list) < self.player1.plant_num and not any(plant.tile_x == player_tile_x and plant.tile_y == player_tile_y for plant in plant_list):
                    plant_list.append(Plant(player_tile_x, player_tile_y))
                    self.player2.placed_water = 1

            # 更新炸彈和植物狀態
            for bomb in bombs_list:
                bomb.update(self.game_map.grid, [self.player1, self.player2])

            for plant in plant_list:
                plant.update(self.game_map.grid)

            # 移除已爆炸的炸彈和已成長的植物
            bombs_list = [bomb for bomb in bombs_list if not bomb.is_finished()]
            plant_list = [plant for plant in plant_list if not plant.is_finished()]

            # 繪製地圖
            self.game_map.draw(self.screen, {
                TileType.UNBREAKABLE: tile_unbreakable_img,
                TileType.BREAKABLE: tile_breakable_img,
                TileType.AROUND: tile_around_img,
                TileType.BUFF_NUM: tile_buff_num_img,
                TileType.BUFF_RANGE: tile_buff_range_img,
                TileType.HEAL: tile_heal_img,
                TileType.GRASS_BUFF_NUM: tile_breakable_img,
                TileType.GRASS_BUFF_RANGE: tile_breakable_img,
                TileType.GRASS_HEAL: tile_breakable_img,
                TileType.WATER: tile_water_img
            })

            # 繪製分數板
            self.scoreboard.draw(self.screen)

            # 繪製植物
            for plant in plant_list:
                plant.draw(self.screen)

            self.player1.update_animation()
            self.player1.draw(self.screen)

            self.player2.update_animation()
            self.player2.draw(self.screen)
            
            # 繪製炸彈
            for bomb in bombs_list:
                bomb.draw(self.screen)
            
            # 縮小地圖邊界
            self.game_map.shrink_map()

            if (self.player1.heal <= 0 or self.player2.heal <= 0):
                self.state = "gameover"

            if keyboard.is_pressed('p'):
                self.p_count += 1
                print(f"p_count: {self.p_count}")
                pygame.time.wait(150)

            
            if self.p_count == 2:
                self.reset()
                self.state = "start"
                pygame.time.wait(150)

            pygame.display.flip()
            self.clock.tick(30)
            self.check_quit()

    def gameover_screen(self):
        while self.state == "gameover":
            # self.screen.fill((BLACK))

            # 判斷贏家並顯示文字
            if self.player1.heal <= 0 and self.player2.heal > 0:
                winner_text = title_font.render(f"{self.player2.name} Wins!", True, WHITE)
            elif self.player2.heal <= 0 and self.player1.heal > 0:
                winner_text = title_font.render(f"{self.player1.name} Wins!", True, WHITE)
            else:
                winner_text = title_font.render("BOTH DEATH !!!", True, WHITE)
            self.screen.blit(winner_text, (GAME_WIDTH // 2 - winner_text.get_width() // 2, SCREEN_HEIGHT // 2 - winner_text.get_height() // 2 - 50))

            # 顯示 Game Over
            game_over_text = title_font.render("Game Over", True, WHITE)
            self.screen.blit(game_over_text, (GAME_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

            # 顯示 restart 提示
            retry_text = font.render("Press 'R' to Restart", True, WHITE)
            self.screen.blit(retry_text, (GAME_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 200))

            # 顯示 goto Start Page 提示
            start_text = font.render("Press 'P' goto Start Page", True, WHITE)
            self.screen.blit(start_text, (GAME_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 230))

            # 按 p 返回開始畫面
            if keyboard.is_pressed("p"):
                print("goto start screen")
                self.state = "start"
                pygame.time.wait(150)

            # 按 r 重新開始遊戲
            elif keyboard.is_pressed("r"):
                print("replay game")
                self.reset()
                self.state = "game"
                pygame.time.wait(150)

            self.clock.tick(60)
            pygame.display.flip()

            self.check_quit()

    # def pause_screen(self):
    #     puase_text = title_font.render("PAUSE", True, WHITE)
    #     self.screen.blit(puase_text, (GAME_WIDTH // 2 - puase_text.get_width() // 2, SCREEN_HEIGHT // 2 - puase_text.get_height() // 2))
    #     if keyboard.is_pressed("p"):
    #         self.state = "game"
    #         pygame.time.wait(150)

    #     self.clock.tick(60)
    #     pygame.display.flip()
    #     self.check_quit()
    

    # 處理輸入
    def handle_input(self, field):
        for char in "abcdefghijklmnopqrstuvwxyz0123456789":
            if keyboard.is_pressed(char):
                if field == "player1" and len(self.player1.name) < 8:
                    self.player1.name += char.upper()
                elif field == "player2" and len(self.player2.name) < 8:
                    self.player2.name += char.upper()
                pygame.time.wait(150)

        if keyboard.is_pressed("backspace"):
            if field == "player1" and self.player1.name:
                self.player1.name = self.player1.name[:-1]
            elif field == "player2" and self.player2.name:
                self.player2.name = self.player2.name[:-1]
            pygame.time.wait(150)

    # 檢查退出
    def check_quit(self):
        # 按 esc 退出遊戲
        if keyboard.is_pressed('esc'):
            self.running = False
            pygame.quit()
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()         

    def run(self):
        while self.running:
            if self.state == "start":
                self.start_screen()
            elif self.state == "game":
                self.game_loop()
            elif self.state == "gameover":
                self.gameover_screen()
            elif self.state == "pause":
                self.pause_screen()