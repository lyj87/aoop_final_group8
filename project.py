import pygame
import random

# 初始化pygame
pygame.init()

# 常量定义
TILE_SIZE = 32
GRID_SIZE = 20  # 调整到更适合窗口的规模
SCREEN_WIDTH = GRID_SIZE * TILE_SIZE
SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)

# 初始化屏幕
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("64x64 Map Game")

# 石块类型
class TileType:
    UNBREAKABLE = 0
    BREAKABLE = 1
    EMPTY = 2

# 玩家类
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = RED
        self.last_move_time = 0  # 上次移动的时间
        self.move_cooldown = 200  # 两次移动之间的时间间隔（毫秒）

    def can_move(self):
        # 检查是否冷却时间已过
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.move_cooldown:
            self.last_move_time = current_time
            return True
        return False

    def move(self, dx, dy, grid):
        if self.can_move():
            new_x = self.x + dx
            new_y = self.y + dy
            if 0 <= new_x < GRID_SIZE and 0 <= new_y < GRID_SIZE:
                if grid[new_y][new_x] == TileType.EMPTY:
                    self.x = new_x
                    self.y = new_y


    def break_tile(self, grid):
        # 获取玩家面前的格子坐标
        target_x, target_y = self.x, self.y
        if grid[target_y][target_x] == TileType.BREAKABLE:
            grid[target_y][target_x] = TileType.EMPTY

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
                    self.grid[y][x] = TileType.UNBREAKABLE
                elif x % 2 == 0 and y % 2 == 0:
                    self.grid[y][x] = TileType.UNBREAKABLE
                else:
                    # 随机生成可破坏的石块
                    if random.random() < 0.2:
                        self.grid[y][x] = TileType.BREAKABLE

    def draw(self, screen):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] == TileType.UNBREAKABLE:
                    color = GRAY
                elif self.grid[y][x] == TileType.BREAKABLE:
                    color = WHITE
                else:
                    continue
                pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# 主游戏逻辑
def main():
    clock = pygame.time.Clock()
    running = True

    game_map = Map()
    player = Player(1, 1)

    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player.move(0, -1, game_map.grid)
        if keys[pygame.K_s]:
            player.move(0, 1, game_map.grid)
        if keys[pygame.K_a]:
            player.move(-1, 0, game_map.grid)
        if keys[pygame.K_d]:
            player.move(1, 0, game_map.grid)
        if keys[pygame.K_q]:
            player.break_tile(game_map.grid)

        game_map.draw(screen)
        pygame.draw.rect(screen, player.color, (player.x * TILE_SIZE, player.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
