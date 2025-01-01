import pygame
import keyboard

from player import Player
from map import Map
from bomb import Bomb
from scoreboard import Scoreboard
from constant import *

pygame.init()

screen = pygame.display.set_mode((GRID_SIZE * TILE_SIZE + SCOREBOARD_WIDTH, GRID_SIZE * TILE_SIZE))
pygame.display.set_caption("Game")

assets_img = pygame.image.load("./assets/assets.png")

background_img = pygame.image.load("./assets/background.png")
background_img = pygame.transform.scale(background_img, (TILE_SIZE, TILE_SIZE))

tile_around_img = assets_img.subsurface(10 * 32, 18 * 32, 32, 32)
tile_around_img = pygame.transform.scale(tile_around_img, (TILE_SIZE, TILE_SIZE))

# tile_unbreakable_img = pygame.image.load("./assets/stone.png")
tile_unbreakable_img = assets_img.subsurface(10 * 32, 17 * 32, 32, 32)
tile_unbreakable_img = pygame.transform.scale(tile_unbreakable_img, (TILE_SIZE, TILE_SIZE))

# tile_breakable_img = pygame.image.load("./assets/assets.png")
tile_breakable_img = assets_img.subsurface(9 * 32, 13 * 32, 32, 32)
tile_breakable_img = pygame.transform.scale(tile_breakable_img, (TILE_SIZE, TILE_SIZE))

player_img = pygame.image.load("./assets/player.png")
player_frames = {
    "DOWN": [],
    "RIGHT": [],
    "LEFT": [],
    "UP": []
}
for i in range(6):  # 6 frames per direction
    player_frames["DOWN"].append(player_img.subsurface((i * 32, 3 * 32, 32, 32)))
    player_frames["RIGHT"].append(player_img.subsurface((i * 32, 4 * 32, 32, 32)))
    player_frames["LEFT"].append(player_img.subsurface((i * 32, 4 * 32, 32, 32)))
    player_frames["UP"].append(player_img.subsurface((i * 32, 5 * 32, 32, 32)))

clock = pygame.time.Clock()

def main():
    running = True

    game_map = Map()
    player = Player(1, 1, player_frames)
    player2 = Player(GRID_SIZE -2 , GRID_SIZE - 2, player_frames)
    bombs = []
    bombs2 = []
    scoreboard = Scoreboard([player, player2])

    while running:
        for y in range(1, GRID_SIZE - 1):
            for x in range(1, GRID_SIZE - 1):
                screen.blit(background_img, (x * TILE_SIZE, y * TILE_SIZE))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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
            if not any(bomb.tile_x == player_tile_x and bomb.tile_y == player_tile_y for bomb in bombs):
                # 调整爆炸范围到 3 格
                bombs.append(Bomb(player_tile_x, player_tile_y, player.explosion_range, player))

        if keyboard.is_pressed('e') and not key_pressed:
            key_pressed = True  # 设置为已触发
            player.explosion_range += 1
        elif not keyboard.is_pressed('e'):
            key_pressed = False  # 当按键松开时，重置状态

        # 放置炸弹
        if keyboard.is_pressed('shift'):
            player2_tile_x = (player2.x + 8) // TILE_SIZE
            player2_tile_y = (player2.y + 8) // TILE_SIZE
            if not any(bomb2.tile_x == player2_tile_x and bomb2.tile_y == player2_tile_y for bomb2 in bombs):
                # 调整爆炸范围到 3 格
                bombs.append(Bomb(player2_tile_x, player2_tile_y, player2.explosion_range, player))

        # 更新炸弹状态
        for bomb in bombs:
            bomb.update(game_map.grid, [player, player2])
            if bomb.exploded:
                bomb.explosion(game_map.grid, [player, player2])

        for bomb in bombs2:
            bomb.update(game_map.grid, [player, player2])
            if bomb.exploded:
                bomb.explosion(game_map.grid, [player, player2])

        # 移除已完成的炸弹
        bombs = [bomb for bomb in bombs if not bomb.is_finished()]
        bombs2 = [bomb for bomb in bombs2 if not bomb.is_finished()]

        # 绘制地图和角色
        screen.fill(BLACK)
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                screen.blit(background_img, (x * TILE_SIZE, y * TILE_SIZE))

        game_map.draw(screen, {
            TileType.UNBREAKABLE: tile_unbreakable_img,
            TileType.BREAKABLE: tile_breakable_img,
            TileType.AROUND: tile_around_img
        })
        scoreboard.draw(screen)
        player.update_animation()
        player.draw(screen)
        player2.draw(screen)

        # 绘制炸弹
        for bomb in bombs:
            bomb.draw(screen)

        for bomb in bombs2:
            bomb.draw(screen)

        if keyboard.is_pressed('esc'):
            running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    
if __name__ == "__main__":
    main()