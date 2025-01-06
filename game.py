import pygame
import sys

from constant import *
from player import Player
from map import Map
from bomb import Bomb
from scoreboard import Scoreboard
from plant import Plant
from page import Page

class Game(Page):
    def __init__(self, screen, player1_name, player2_name):
        super().__init__(screen)
        # 字體
        self.font = pygame.font.SysFont('notosanscjktc', 36)
        self.title_font = pygame.font.SysFont('Arial', 84)
        self.puase_font = pygame.font.SysFont('Arial', 300)

        # 畫
        pygame.display.set_caption(f"{GRID_SIZE}x{GRID_SIZE} Map Game")
        self.clock = pygame.time.Clock()

        # 遊戲狀態
        self.state = "game"  

        # 玩家對象
        self.game_map = Map()
        self.player1 = Player(1, 1, player1_name, player1_frames)
        self.player2 = Player(GRID_SIZE - 2, GRID_SIZE - 2, player2_name, player2_frames)
        self.scoreboard = Scoreboard([self.player1, self.player2], self.game_map)
        self.bombs_list = []
        self.plant_list = []
        self.clock = pygame.time.Clock()
        
    def pause_screen(self):
        while self.state == "pause":
            # 畫暫停畫面
            pause_text = self.title_font.render("PAUSE", True, WHITE)
            self.screen.blit(pause_text, 
                            (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 - pause_text.get_height() // 2))
            
            # 提示選項
            retry_text = self.font.render("Press 'R' to Restart", True, WHITE)
            self.screen.blit(retry_text, 
                            (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 50))
            start_text = self.font.render("Press 'P' to Resume Game", True, WHITE)
            self.screen.blit(start_text, 
                            (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 100))
            exit_text = self.font.render("Press 'ESC' to Exit", True, WHITE)
            self.screen.blit(exit_text, 
                            (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 
                            SCREEN_HEIGHT // 2 + 150))
            
            pygame.display.flip()  # 更新畫面
            
            # 單獨處理暫停時的事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # 重置遊戲狀態，重新開始
                        self.state = "start"
                        print("Restarting game...")
                        return
                    elif event.key == pygame.K_p:
                        # 返回遊戲
                        self.state = "game"
                        print("Resuming game...")
                        return
                    elif event.key == pygame.K_ESCAPE:
                        # 退出遊戲
                        pygame.quit()
                        sys.exit()

    def game_loop(self):
        #self.state = "game"
        while self.state == "game":
            # 繪製地圖
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    self.screen.blit(background_img, (x * TILE_SIZE, y * TILE_SIZE))

            keys = pygame.key.get_pressed()

            # player1 移動
            dx, dy = 0, 0
            if keys[pygame.K_w]:
                dy = -1
            if keys[pygame.K_s]:
                dy = 1
            if keys[pygame.K_a]:
                dx = -1
            if keys[pygame.K_d]:
                dx = 1
            self.player1.move(dx, dy, self.game_map.grid)

            # player2 移動
            dx2, dy2 = 0, 0
            if keys[pygame.K_UP]:
                dy2 = -1
            if keys[pygame.K_DOWN]:
                dy2 = 1
            if keys[pygame.K_LEFT]:
                dx2 = -1
            if keys[pygame.K_RIGHT]:
                dx2 = 1
            self.player2.move(dx2, dy2, self.game_map.grid)

            # player 1 放置炸彈
            if keys[pygame.K_f]:
                player_tile_x = (self.player1.x + 8) // TILE_SIZE
                player_tile_y = (self.player1.y + 8) // TILE_SIZE
                if len(self.bombs_list) < self.player1.bomb_num and not any(bomb.tile_x == player_tile_x and bomb.tile_y == player_tile_y for bomb in self.bombs_list):
                    self.bombs_list.append(Bomb(player_tile_x, player_tile_y, self.player1.explosion_range, self.player1))
                    self.player1.placed_bomb = 1

            # player 1 放置植物
            if keys[pygame.K_g]:
                player_tile_x = (self.player1.x + 8) // TILE_SIZE
                player_tile_y = (self.player1.y + 8) // TILE_SIZE
                if len(self.plant_list) < self.player1.plant_num and not any(plant.tile_x == player_tile_x and plant.tile_y == player_tile_y for plant in self.plant_list):
                    self.plant_list.append(Plant(player_tile_x, player_tile_y))
                    self.player1.placed_water = 1

            # player 2 放置炸彈
            if keys[pygame.K_m]:
                player2_tile_x = (self.player2.x + 8) // TILE_SIZE
                player2_tile_y = (self.player2.y + 8) // TILE_SIZE
                if len(self.bombs_list) < self.player2.bomb_num and not any(bomb.tile_x == player2_tile_x and bomb.tile_y == player2_tile_y for bomb in self.bombs_list):
                    self.bombs_list.append(Bomb(player2_tile_x, player2_tile_y, self.player2.explosion_range, self.player2))
                    self.player2.placed_bomb = 1

            if keys[pygame.K_n]:
                player_tile_x = (self.player2.x + 8) // TILE_SIZE
                player_tile_y = (self.player2.y + 8) // TILE_SIZE
                if len(self.plant_list) < self.player1.plant_num and not any(plant.tile_x == player_tile_x and plant.tile_y == player_tile_y for plant in self.plant_list):
                    self.plant_list.append(Plant(player_tile_x, player_tile_y))
                    self.player2.placed_water = 1

            # 更新炸彈和植物狀態
            for bomb in self.bombs_list:
                bomb.update(self.game_map.grid, [self.player1, self.player2])

            for plant in self.plant_list:
                plant.update(self.game_map.grid)

            # 移除已爆炸的炸彈和已成長的植物
            self.bombs_list = [bomb for bomb in self.bombs_list if not bomb.is_finished()]
            self.plant_list = [plant for plant in self.plant_list if not plant.is_finished()]

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
            for plant in self.plant_list:
                plant.draw(self.screen)

            self.player1.update_animation()
            self.player1.draw(self.screen)

            self.player2.update_animation()
            self.player2.draw(self.screen)
            
            # 繪製炸彈
            for bomb in self.bombs_list:
                bomb.draw(self.screen)
            
            # 縮小地圖邊界
            self.game_map.shrink_map()

            if self.player1.heal <= 0 or self.player2.heal <= 0:
                self.state = "gameover"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.state = "pause"

            if self.state == "pause":
                print("pause")
                self.pause_screen()
                # 移除並重新添加炸彈和植物
                self.bombs_list = [Bomb(bomb.tile_x, bomb.tile_y, bomb.explosion_range, bomb.owner) for bomb in self.bombs_list]
                self.plant_list = [Plant(plant.tile_x, plant.tile_y) for plant in self.plant_list]
                continue  # 返回後跳過當前更新

            pygame.display.flip()
            self.clock.tick(30)

        self.clock.tick(60)
        pygame.display.flip()
    

# if __name__ == "__main__":
#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     game = Game(screen, "player1", "player2")
#     game.game_loop()
#     pygame.quit()
#     sys.exit()
