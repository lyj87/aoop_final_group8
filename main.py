import pygame
import keyboard
# import time

from player import Player
from map import Map
from bomb import Bomb
from scoreboard import Scoreboard
from plant import Plant
from constant import *

pygame.init()
pygame.display.set_caption(f"{GRID_SIZE}x{GRID_SIZE} Map Game")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def main():
    
    running = True

    game_map = Map()
    player = Player(1, 1, player_frames, explosion_range = 1, score = 0, heal = 2, bomb_num = 1)
    # player2 = Player(GRID_SIZE - 2 , GRID_SIZE - 2, player_frames, explosion_range = 1, score = 0, heal = 2, bomb = 1)
    player2 = Player(2 , 1, player_frames, explosion_range = 1, score = 0, heal = 2, bomb_num = 1)
    bombs_list = []
    bombs2_list = []
    plant_list = []
    scoreboard = Scoreboard([player, player2])
    # # 初始化计时器
    # # start_time = time.time()

    while running:
        for y in range(1, GRID_SIZE - 1):
            for x in range(1, GRID_SIZE - 1):
                screen.blit(background_img, (x * TILE_SIZE, y * TILE_SIZE))
        
    #     # game_map.shrink_map

    #     # current_time = time.time()
    #     # if current_time - start_time >= 5:  # 每隔150秒执行一次
    #     #     game_map.shrink_map()
    #     #     start_time = current_time  # 重置计时器

        dx, dy = 0, 0
        if keyboard.is_pressed('w'):
            dy = -1
        if keyboard.is_pressed('s'):
            dy = 1
        if keyboard.is_pressed('a'):
            dx = -1
        if keyboard.is_pressed('d'):
            dx = 1
        player.move(dx, dy, game_map.grid)

        dx2, dy2 = 0, 0
        if keyboard.is_pressed('up'):
            dy2 = -1
        if keyboard.is_pressed('down'):
            dy2 = 1
        if keyboard.is_pressed('left'):
            dx2 = -1
        if keyboard.is_pressed('right'):
            dx2 = 1
        player2.move(dx2, dy2, game_map.grid)

        # 放置炸弹
        if keyboard.is_pressed('q'):
            # +8是爲了補償player.cheak_collision的偏移
            player_tile_x = (player.x + 8) // TILE_SIZE
            player_tile_y = (player.y + 8) // TILE_SIZE
            if len(bombs_list) < player.bomb_num and not any(bomb.tile_x == player_tile_x and bomb.tile_y == player_tile_y for bomb in bombs_list):
                bombs_list.append(Bomb(player_tile_x, player_tile_y, player.explosion_range, player))
                player.placed_bomb = 1

        if keyboard.is_pressed('e'):
            # +8是爲了補償player.cheak_collision的偏移
            player_tile_x = (player.x + 8) // TILE_SIZE
            player_tile_y = (player.y + 8) // TILE_SIZE
            if not any(plant.tile_x == player_tile_x and plant.tile_y == player_tile_y for plant in plant_list):
                plant_list.append(Plant(player_tile_x, player_tile_y))
                player.placed_water = 1

        # if keyboard.is_pressed('t') and not key_pressed:
        #     key_pressed = True  # 设置为已触发
        #     player.explosion_range += 1
        # elif not keyboard.is_pressed('e'):
        #     key_pressed = False  # 当按键松开时，重置状态

        # 放置炸弹
        if keyboard.is_pressed('shift'):
            player2_tile_x = (player2.x + 8) // TILE_SIZE
            player2_tile_y = (player2.y + 8) // TILE_SIZE
            if len(bombs_list) < player2.bomb_num and not any(bomb.tile_x == player2_tile_x and bomb.tile_y == player2_tile_y for bomb in bombs2_list):
                # 调整爆炸范围到 3 格
                bombs2_list.append(Bomb(player2_tile_x, player2_tile_y, player2.explosion_range, player2))
                player2.placed_bomb = 1

        if keyboard.is_pressed('/'):
            # +8是爲了補償player.cheak_collision的偏移
            player2_tile_x = (player2.x + 8) // TILE_SIZE
            player2_tile_y = (player2.y + 8) // TILE_SIZE
            if not any(plant.tile_x == player2_tile_x and plant.tile_y == player2_tile_y for plant in plant_list):
                plant_list.append(Plant(player2_tile_x, player2_tile_y))
                player.placed_water = 1

        # 更新炸弹状态
        for bomb in bombs_list:
            bomb.update(game_map.grid, [player, player2])

        for bomb in bombs2_list:
            bomb.update(game_map.grid, [player, player2])

        for plant in plant_list:
            plant.update(game_map.grid)

        # 移除已完成的炸弹
        bombs_list = [bomb for bomb in bombs_list if not bomb.is_finished()]
        bombs2_list = [bomb for bomb in bombs2_list if not bomb.is_finished()]

        # 绘制地图和角色
        screen.fill(BLACK)
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                screen.blit(background_img, (x * TILE_SIZE, y * TILE_SIZE))

        game_map.draw(screen, {
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
        scoreboard.draw(screen)
        
        for plant in plant_list:
            plant.draw(screen)

        player.update_animation()
        player.draw(screen)

        player2.update_animation()
        player2.draw(screen)

        # 绘制炸弹
        for bomb in bombs_list:
            bomb.draw(screen)

        for bomb in bombs2_list:
            bomb.draw(screen)
        
        if keyboard.is_pressed('esc'):
            running = False

        if player.heal <= 0 or player2.heal <= 0:
            screen.fill((0, 0, 0))  # 清空屏幕
            font = pygame.font.SysFont("Arial", 36)

            # 创建“Game Over”文字
            game_over_text = font.render("Game Over", True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 50))
            screen.blit(game_over_text, game_over_rect)

            # 创建重玩提示文字
            retry_text = font.render("Press 'R' to Restart", True, WHITE)
            retry_rect = retry_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 50))
            screen.blit(retry_text, retry_rect)

            pygame.display.flip()  # 更新屏幕
            # pygame.time.wait(2000)  # 等待2秒后关闭
            # running = False

        if keyboard.is_pressed('r'):
            main()  # 递归调用重新开始游戏

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    return False
    
if __name__ == "__main__":
    main()
    # while True:
        # if not main():  # 如果游戏结束，退出程序
        #     break