import pygame
from constant import *

bomb_img = pygame.image.load("./assets/assets.png")
bomb_frames = []
for i in range(4, 10):
    bomb_frames.append(bomb_img.subsurface((i * IMG_SIZE, 18 * IMG_SIZE, IMG_SIZE, IMG_SIZE)))

explosion_img = pygame.image.load("./assets/explosion.png")
explosion_img = pygame.transform.scale (explosion_img, (TILE_SIZE, TILE_SIZE))

class Bomb:
    def __init__(self, x, y, explosion_range, owner):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.tile_x = x
        self.tile_y = y
        self.timer = 90  # 爆炸倒计时 3 秒（30 幀/秒）
        self.exploded = False
        self.explosion_range = explosion_range
        self.owner = owner  # 炸弹的主人

        # self.explosion_img = explosion_img
        self.explosion_frames = explosion_img
        self.explosion_timer = 12  # 爆炸动画持续时间
        self.explosion_effects = []  # 存放爆炸范围内的火焰动画

        
        self.bomb_frames = bomb_frames
        self.bomb_frame_index = 0
        self.animation_counter = 0  # 动画计数器
        self.animation_speed = 15  # 每隔5帧（0.5秒）更新一次动画帧

        self.damaged_players = []  # 记录已受伤的玩家，确保伤害只生效一次

    def update(self, grid, players):
        if self.timer > 0:
            grid[self.tile_x][self.tile_y] = TileType.BOMB  # 标记炸弹位置
            self.timer -= 1
            # 更新炸弹动画帧
            self.animation_counter += 1
            if self.animation_counter >= self.animation_speed:
                self.bomb_frame_index = (self.bomb_frame_index + 1) % len(self.bomb_frames)
                self.animation_counter = 0  # 重置计数器
        elif not self.exploded:
            self.exploded = True
            grid[self.tile_x][self.tile_y] = TileType.EMPTY  # 爆炸后清除炸弹
            self.explosion(grid, players)

    def explosion(self, grid, players):
        # 爆炸逻辑：清除范围内的可破坏砖块，并记录爆炸效果位置
        directions = [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]  # 上下左右
        self.explosion_effects.append((self.tile_x, self.tile_y))  # 添加炸弹中心

        # 检查爆炸范围
        for dx, dy in directions:
            for step in range(1, self.explosion_range + 1):
                nx, ny = self.tile_x + dx * step, self.tile_y + dy * step
                # 检查边界条件
                if not (1 <= nx <= GRID_SIZE - 2 and 1 <= ny <= GRID_SIZE - 2):
                    break
                # 根据不同的格子类型处理
                elif grid[nx][ny] == TileType.UNBREAKABLE or grid[nx][ny] == TileType.AROUND:
                    break  # 遇到不可破坏砖块或边界，停止传播
                elif grid[nx][ny] == TileType.BREAKABLE:
                    grid[nx][ny] = TileType.EMPTY  # 清除可破坏砖块
                    self.explosion_effects.append((nx, ny))  # 添加爆炸位置
                    break  # 停止当前方向传播
                elif grid[nx][ny] == TileType.GRASS_BUFF_NUM:
                    grid[nx][ny] = TileType.BUFF_NUM
                    self.explosion_effects.append((nx, ny))  # 添加爆炸位置
                    break
                elif grid[nx][ny] == TileType.GRASS_BUFF_RANGE:
                    grid[nx][ny] = TileType.BUFF_RANGE
                    self.explosion_effects.append((nx, ny))  # 添加爆炸位置
                    break
                elif grid[nx][ny] == TileType.GRASS_HEAL:
                    grid[nx][ny] = TileType.HEAL
                    self.explosion_effects.append((nx, ny))  # 添加爆炸位置
                    break
                else:
                    self.explosion_effects.append((nx, ny))  # 添加普通爆炸范围

        # 检测爆炸范围内是否击中玩家
        for dx, dy in directions:
            for step in range(1, self.explosion_range + 1):
                nx, ny = self.tile_x + dx * step, self.tile_y + dy * step
                # 检查边界条件
                if not (1 <= nx <= GRID_SIZE - 2 and 1 <= ny <= GRID_SIZE - 2):
                    break
                for player in players:
                    player_tile_x = (player.x + 8) // TILE_SIZE  # 补偿偏移量
                    player_tile_y = (player.y + 8) // TILE_SIZE
                    if (player_tile_x, player_tile_y) == (nx, ny):
                        self.apply_damage(player)

    def apply_damage(self, player):
        # """对玩家造成伤害，并增加得分（仅一次）"""
        if player not in self.damaged_players:
            player.heal -= 1  # 玩家生命值减1
            self.damaged_players.append(player)  # 记录该玩家已受伤
            if player != self.owner:  # 如果受伤玩家不是炸弹主人
                self.owner.score += 1  # 炸弹主人得分

    def draw(self, screen):
        if self.timer > 0:
            # 绘制炸弹动画帧
            current_bomb_frame = self.bomb_frames[self.bomb_frame_index]
            screen.blit(current_bomb_frame, (self.x, self.y))
        elif self.explosion_timer > 0:
            # 绘制爆炸效果
            # frame_index = (15 - self.explosion_timer) // 5  # 每 5 帧切换一张图片
            for effect_x, effect_y in self.explosion_effects:
                screen.blit(self.explosion_frames, (effect_x * TILE_SIZE, effect_y * TILE_SIZE))
            
            for damage_player in self.damaged_players:
                damage_player.damage_draw(screen)

            self.explosion_timer -= 1

            

    def is_finished(self):
        return self.exploded and self.explosion_timer <= 0