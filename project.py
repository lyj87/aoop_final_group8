import pygame
import random
import keyboard

# 初始化pygame
pygame.init()

# 常量定义
TILE_SIZE = 40
GRID_SIZE = 40  # 游戏地图的网格大小
SCOREBOARD_WIDTH = 250  # 计分板宽度
SCREEN_WIDTH = GRID_SIZE * TILE_SIZE + SCOREBOARD_WIDTH
SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 初始化屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(f"{GRID_SIZE}x{GRID_SIZE} Map Game")

# 加载图片资源
background_img = pygame.image.load("./assets/background.png")
tile_unbreakable_img = pygame.image.load("./assets/stone.png")
tile_breakable_img = pygame.image.load("./assets/grass.png")
player_img = pygame.image.load("./assets/player.png")

# 调整图片大小
background_img = pygame.transform.scale(background_img, (TILE_SIZE, TILE_SIZE))
tile_unbreakable_img = pygame.transform.scale(tile_unbreakable_img, (TILE_SIZE, TILE_SIZE))
tile_breakable_img = pygame.transform.scale(tile_breakable_img, (TILE_SIZE, TILE_SIZE))
player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

# 石块类型
class TileType:
    UNBREAKABLE = 0
    BREAKABLE = 1
    EMPTY = 2

# 玩家类
class Player:
    def __init__(self, x, y):
        self.x = x * TILE_SIZE  # 转换为像素坐标
        self.y = y * TILE_SIZE
        self.speed = 20  # 每帧移动的像素距离
        self.image = player_img
        self.direction = "DOWN"  # 初始方向为向下
        self.score = 0
        self.explosion_range = 1  # 初始爆炸范围为 1 格

    def set_direction(self, dx, dy):
        if dx > 0:
            self.direction = "RIGHT"
        elif dx < 0:
            self.direction = "LEFT"
        elif dy > 0:
            self.direction = "DOWN"
        elif dy < 0:
            self.direction = "UP"

    def move(self, dx, dy, grid):
        # 更新方向
        self.set_direction(dx, dy)

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        if self.check_collision(new_x, new_y, dx, dy, grid):
            self.x = new_x
            self.y = new_y

    def check_collision(self, new_x, new_y, dx, dy, grid):
        # 角色四个角的像素坐标
        corners = [
            (new_x, new_y), # 左上角
            (new_x + TILE_SIZE - 1, new_y), # 右上角
            (new_x, new_y + TILE_SIZE - 1), # 左下角
            (new_x + TILE_SIZE - 1, new_y + TILE_SIZE - 1), # 右下角
        ]

        for corner in corners:
            x = corner[0] // TILE_SIZE
            y = corner[1] // TILE_SIZE
            if (grid[x][y] != TileType.EMPTY):  # 如果角点处是障碍物
                return False
        return True

    def draw(self, screen):
        # 根据方向绘制角色图片
        if self.direction == "UP":
            rotated_image = pygame.transform.rotate(self.image, 90)
        elif self.direction == "DOWN":
            rotated_image = pygame.transform.rotate(self.image, -90)
        elif self.direction == "LEFT":
            rotated_image = pygame.transform.flip(self.image, True, False)
        else:  # "RIGHT"
            rotated_image = self.image

        screen.blit(rotated_image, (self.x, self.y))


# 游戏地图
class Map:
    def __init__(self):
        self.grid = [[TileType.EMPTY for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.generate_map()

    def generate_map(self):
        # 边缘设置为不可破坏的石块
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if x == 0 or x == GRID_SIZE - 1 or y == 0 or y == GRID_SIZE - 1:
                    self.grid[x][y] = TileType.UNBREAKABLE
                elif x % 2 == 0 and y % 2 == 0 and not (x == GRID_SIZE-2 and y == GRID_SIZE-2):
                    self.grid[x][y] = TileType.UNBREAKABLE
                else:
                    # 随机生成可破坏的石块
                    if random.random() < 0.2 and not (x == 1 and y == 1) and not (x == GRID_SIZE-2 and y == GRID_SIZE-2):
                        self.grid[x][y] = TileType.BREAKABLE

    def draw(self, screen):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[x][y] == TileType.UNBREAKABLE:
                    screen.blit(tile_unbreakable_img, (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[x][y] == TileType.BREAKABLE:
                    screen.blit(tile_breakable_img, (x * TILE_SIZE, y * TILE_SIZE))

# 炸彈
class Bomb:
    def __init__(self, x, y, explosion_range):
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.tile_x = x
        self.tile_y = y
        self.timer = 90  # 爆炸倒计时 3 秒（30 帧/秒）
        self.timer = 60  # 爆炸倒计时 2 秒（30 帧/秒）
        self.exploded = False
        self.explosion_range = explosion_range
        self.image = pygame.image.load("./assets/bomb.jpg")
        self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
        self.explosion_frames = [pygame.image.load(f"./assets/explosion_{i}.png") for i in range(1, 4)]
        self.explosion_frames = [pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE)) for frame in self.explosion_frames]
        self.explosion_timer = 15  # 爆炸动画持续时间
        self.explosion_effects = []  # 存放爆炸范围内的火焰动画

    def update(self, grid):
        if self.timer > 0:
            self.timer -= 1
        elif not self.exploded:
            self.exploded = True
            self.explosion(grid)

    def explosion(self, grid):
        # 爆炸逻辑：清除范围内的可破坏砖块，并记录爆炸效果位置
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # 上下左右
        self.explosion_effects.append((self.tile_x, self.tile_y))  # 添加炸弹中心

        for dx, dy in directions:
            for step in range(1, self.explosion_range + 1):
                nx, ny = self.tile_x + dx * step, self.tile_y + dy * step
                if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                    if grid[nx][ny] == TileType.UNBREAKABLE:
                        break  # 遇到不可破坏砖块，停止传播
                    self.explosion_effects.append((nx, ny))  # 添加到爆炸范围
                    if grid[nx][ny] == TileType.BREAKABLE:
                        grid[nx][ny] = TileType.EMPTY  # 清除可破坏砖块
                        break  # 停止进一步传播

    def draw(self, screen):
        if self.timer > 0:
            screen.blit(self.image, (self.x, self.y))
        elif self.explosion_timer > 0:
            # 绘制爆炸效果
            frame_index = (15 - self.explosion_timer) // 5  # 每 5 帧切换一张图片
            explosion_frame = self.explosion_frames[frame_index]
            for effect_x, effect_y in self.explosion_effects:
                screen.blit(explosion_frame, (effect_x * TILE_SIZE, effect_y * TILE_SIZE))
            self.explosion_timer -= 1

    def is_finished(self):
        return self.exploded and self.explosion_timer <= 0
    
# 計分板
class Scoreboard:
    def __init__(self, player, player2):
        self.player = player
        self.player2 = player2
        self.font = pygame.font.SysFont("Arial", 24)
        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)
        self.subtitle_font = pygame.font.SysFont("Arial", 24, bold=True)

    def draw(self, screen):
        # 繪製計分板
        pygame.draw.rect(screen, GRAY, (GRID_SIZE * TILE_SIZE, 0, SCOREBOARD_WIDTH, SCREEN_HEIGHT))

        # 繪製標題
        title_text = self.title_font.render("Scoreboard", True, WHITE)
        screen.blit(title_text, (GRID_SIZE * TILE_SIZE + 20, 20))

        # 繪製player1分數、爆炸範圍
        text = self.subtitle_font.render(f"Player 1", True, WHITE)
        screen.blit(text, (GRID_SIZE * TILE_SIZE + 20, 60))
    
        score_text = self.font.render(f"Score: {self.player.score}", True, WHITE)
        screen.blit(score_text, (GRID_SIZE * TILE_SIZE + 20, 90))

        explosion_range_text = self.font.render(f"Explosion Range: {self.player.explosion_range}", True, WHITE)
        screen.blit(explosion_range_text, (GRID_SIZE * TILE_SIZE + 20, 120))

        # 繪製player2分數、爆炸範圍
        text2 = self.subtitle_font.render(f"Player 2", True, WHITE)
        screen.blit(text2, (GRID_SIZE * TILE_SIZE + 20, 160))

        score_text2 = self.font.render(f"Score: {self.player2.score}", True, WHITE)
        screen.blit(score_text2, (GRID_SIZE * TILE_SIZE + 20, 190))

        explosion_range_text = self.font.render(f"Explosion Range: {self.player.explosion_range}", True, WHITE)
        screen.blit(explosion_range_text, (GRID_SIZE * TILE_SIZE + 20, 220))

        # 繪製菜單
        menu_text = self.title_font.render("Menu", True, WHITE)
        screen.blit(menu_text, (GRID_SIZE * TILE_SIZE + 20, 280))

        # 菜單選項
        menu_items = ["Player 1","WASD: Move","Q: Place Bomb","","Player 2","Arrow Keys: Move", "Shift: Place Bomb","","ESC: Quit"]
        for i, item in enumerate(menu_items):
            item_text = self.font.render(item, True, WHITE)
            screen.blit(item_text, (GRID_SIZE * TILE_SIZE + 20, 320 + i * 30))

# 碰撞检测
def check_collision(player,bombs, bombs2):
    player_rect = pygame.Rect(player.x, player.y, TILE_SIZE, TILE_SIZE)
    
    for bomb in bombs:
        if bomb.exploded:
            for effect_x, effect_y in bomb.explosion_effects:
                explosion_rect = pygame.Rect(effect_x * TILE_SIZE, effect_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(explosion_rect):
                    return True

    for bomb2 in bombs2:
        if bomb2.exploded:
            for effect_x, effect_y in bomb2.explosion_effects:
                explosion_rect = pygame.Rect(effect_x * TILE_SIZE, effect_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if player_rect.colliderect(explosion_rect):
                    return True
    return False

# 主游戏逻辑
def main():
    clock = pygame.time.Clock()
    running = True

    game_map = Map()
    player = Player(1, 1)
    player2 = Player(GRID_SIZE+GRID_SIZE%2-2, GRID_SIZE+GRID_SIZE%2-2)
    bombs = []
    bombs2 = []
    scoreboard = Scoreboard(player, player2)

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
            player_tile_x = player.x // TILE_SIZE
            player_tile_y = player.y // TILE_SIZE
            if not any(bomb.tile_x == player_tile_x and bomb.tile_y == player_tile_y for bomb in bombs):
                # 调整爆炸范围到 3 格
                bombs.append(Bomb(player_tile_x, player_tile_y, player.explosion_range))

        if keyboard.is_pressed('e') and not key_pressed:
            key_pressed = True  # 设置为已触发
            player.explosion_range += 1
            print(f"Explosion range increased to: {player.explosion_range}")
        elif not keyboard.is_pressed('e'):
            key_pressed = False  # 当按键松开时，重置状态

        # 放置炸弹
        if keyboard.is_pressed('shift'):
            player2_tile_x = player2.x // TILE_SIZE
            player2_tile_y = player2.y // TILE_SIZE
            if not any(bomb2.tile_x == player2_tile_x and bomb2.tile_y == player2_tile_y for bomb2 in bombs):
                # 调整爆炸范围到 3 格
                bombs2.append(Bomb(player2_tile_x, player2_tile_y, player2.explosion_range))

        # 更新炸弹状态
        for bomb in bombs:
            bomb.update(game_map.grid)

        for bomb in bombs2:
            bomb.update(game_map.grid)

        # 移除已完成的炸弹
        bombs = [bomb for bomb in bombs if not bomb.is_finished()]
        bombs2 = [bomb for bomb in bombs2 if not bomb.is_finished()]

        # 绘制地图和角色
        scoreboard.draw(screen)
        game_map.draw(screen)
        player.draw(screen)
        player2.draw(screen)

        # 绘制炸弹
        for bomb in bombs:
            bomb.draw(screen)

        for bomb in bombs2:
            bomb.draw(screen)

        pygame.display.flip()
        clock.tick(30)
        
        if keyboard.is_pressed('esc'):
            running = False

    pygame.quit()
    
if __name__ == "__main__":
    main()