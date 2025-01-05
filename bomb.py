import pygame
from constant import *

# 炸彈圖片
bomb_img = pygame.image.load("./assets/assets.png")
bomb_frames = []
for i in range(4, 10):
    bomb_frames.append(bomb_img.subsurface((i * IMG_SIZE, 18 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))

# 爆炸圖片
explosion_img = pygame.image.load("./assets/explosion.png")
explosion_img = pygame.transform.scale (explosion_img, (TILE_SIZE, TILE_SIZE))

class Bomb:
    def __init__(self, x, y, explosion_range, owner):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.tile_x = x
        self.tile_y = y
        #self.timer = 90  # 爆炸倒计时 3 秒（30 幀/秒）
        self.timer = 60  # 爆炸倒计时 2 秒（30 幀/秒）
        self.exploded = False   # 是否已爆炸
        self.explosion_range = explosion_range  # 爆炸范围
        self.owner = owner  # 炸彈主人
        self.damaged_players = []  # 受傷玩家列表

        # self.explosion_img = explosion_img
        self.explosion_frames = explosion_img
        self.explosion_timer = 12   # 爆炸效果持续时间 0.4 秒（30 幀/秒）
        self.explosion_effects = [] # 爆炸效果位置列表

        self.bomb_frames = bomb_frames
        self.bomb_frame_index = 0   # 炸弹动画帧索引
        self.animation_counter = 0  # 動畫计数器
        self.animation_speed = 15   # 每隔15幀切換一次圖片

    def update(self, grid, players):
        if self.timer > 0:
            grid[self.tile_x][self.tile_y] = TileType.BOMB  # 標記炸彈位置
            self.timer -= 1
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.bomb_frame_index = (self.bomb_frame_index + 1) % len(self.bomb_frames)
                self.animation_counter = 0  # 重置動畫計數器
        elif not self.exploded:
            self.exploded = True
            grid[self.tile_x][self.tile_y] = TileType.EMPTY     #爆炸后清除炸彈位置
            self.explosion(grid, players)

    def explosion(self, grid, players):
        # 爆炸邏輯：清除範圍内的可破壞磚塊，並記錄爆炸效果位置
        directions = [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]  # 中上下左右
        self.explosion_effects.append((self.tile_x, self.tile_y))  # 添加爆炸位置

        # 檢查爆炸範圍
        for dx, dy in directions:
            for step in range(1, self.explosion_range + 1):
                nx, ny = self.tile_x + dx * step, self.tile_y + dy * step
                # 檢查邊界條件
                if not (1 <= nx <= GRID_SIZE - 2 and 1 <= ny <= GRID_SIZE - 2):
                    break
                # 遇到不可破壞的磚塊，停止爆炸
                elif grid[nx][ny] == TileType.UNBREAKABLE or grid[nx][ny] == TileType.AROUND:
                    break
                # 遇到可破壞的磚塊，清除磚塊，添加爆炸位置
                elif grid[nx][ny] == TileType.BREAKABLE:
                    grid[nx][ny] = TileType.EMPTY
                    self.explosion_effects.append((nx, ny))
                    break   # 爆炸停止，保證爆炸范圍不會穿透磚塊
                # 遇到其他物品，添加爆炸位置
                elif grid[nx][ny] == TileType.GRASS_BUFF_NUM:
                    grid[nx][ny] = TileType.BUFF_NUM
                    self.explosion_effects.append((nx, ny))
                    break
                elif grid[nx][ny] == TileType.GRASS_BUFF_RANGE:
                    grid[nx][ny] = TileType.BUFF_RANGE
                    self.explosion_effects.append((nx, ny))
                    break
                elif grid[nx][ny] == TileType.GRASS_HEAL:
                    grid[nx][ny] = TileType.HEAL
                    self.explosion_effects.append((nx, ny))
                    break
                else:
                    self.explosion_effects.append((nx, ny))

        # 檢查爆炸範圍是否擊中角色
        # for dx, dy in directions:
        #     for step in range(1, self.explosion_range + 1):
            for dx, dy in self.explosion_effects:
                nx, ny = dx, dy
                # 檢查邊界條件
                if not (1 <= nx <= GRID_SIZE - 2 and 1 <= ny <= GRID_SIZE - 2):
                    break
                for player in players:
                    # +8為修正玩家位置
                    player_tile_x = (player.x + 8) // TILE_SIZE
                    player_tile_y = (player.y + 8) // TILE_SIZE
                    if (player_tile_x, player_tile_y) == (nx, ny):
                        self.apply_damage(player)

    # 對角色造成傷害
    def apply_damage(self, player):
        # 確保玩家只受到一次傷害
        if player not in self.damaged_players:
            player.heal -= 1  # 玩家生命值減一
            self.damaged_players.append(player)  # 添加到受傷玩家列表
            if player != self.owner:  # 非炸彈主人
                self.owner.score += 1  # 主人得分加一

    def draw(self, screen):
        if self.timer > 0:
            # 繪製炸彈動畫
            current_bomb_frame = self.bomb_frames[self.bomb_frame_index]
            screen.blit(current_bomb_frame, (self.x, self.y))
        elif self.explosion_timer > 0:
            # 繪製爆炸效果
            # frame_index = (15 - self.explosion_timer) // 5  # 每 5 帧切换一张图片
            for effect_x, effect_y in self.explosion_effects:
                screen.blit(self.explosion_frames, (effect_x * TILE_SIZE, effect_y * TILE_SIZE))
            
            # 繪製受傷玩家
            for damage_player in self.damaged_players:
                damage_player.damage_draw(screen)

            self.explosion_timer -= 1

    # 判斷爆炸是否結束
    def is_finished(self):
        return self.exploded and self.explosion_timer <= 0