import pygame
import random
import keyboard

# 初始化pygame
pygame.init()

# 常量定义
TILE_SIZE = 20
GRID_SIZE = 33  # 调整到更适合窗口的规模
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

# 加载图片资源
background_img = pygame.image.load("./assets/background.png")
tile_unbreakable_img = pygame.image.load("./assets/unbreakable_tile.png")
tile_breakable_img = pygame.image.load("./assets/breakable_tile.png")
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
        # self.x = x
        # self.y = y
        # self.image = player_img
        # self.last_move_time = 0  # 上次移动的时间
        # self.move_cooldown = 200  # 两次移动之间的时间间隔（毫秒）
        self.x = x * TILE_SIZE  # 转换为像素坐标
        self.y = y * TILE_SIZE
        self.speed = 4  # 每帧移动的像素距离
        self.image = player_img
        self.direction = "DOWN"  # 初始方向为向下

    def set_direction(self, dx, dy):
        if dx > 0:
            self.direction = "RIGHT"
        elif dx < 0:
            self.direction = "LEFT"
        elif dy > 0:
            self.direction = "DOWN"
        elif dy < 0:
            self.direction = "UP"

    # def move(self, dx, dy, grid):
    #     # 更新方向
    #     self.set_direction(dx, dy)

    #     new_x = self.x + dx * self.speed
    #     new_y = self.y + dy * self.speed
        # print(new_x, new_y)

        # 检测边界和障碍物s
        # grid_x = int(new_x // TILE_SIZE)
        # grid_y = int(new_y // TILE_SIZE)
        # print(grid_x, grid_y)

        # if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
        #     # if grid[grid_y][grid_x] == TileType.EMPTY:
        #         self.x = new_x
        #         self.y = new_y

    def check_collision(self, dx, dy, grid):
        self.set_direction(dx, dy)
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        # 角色四个角的像素坐标
        corners = [
            (new_x, new_y), # 左上角
            (new_x + TILE_SIZE - 1, new_y), # 右上角
            (new_x, new_y + TILE_SIZE - 1), # 左下角
            (new_x + TILE_SIZE - 1, new_y + TILE_SIZE - 1), # 右下角
        ]
        for corner in corners:
            print(corner[0], corner[1])
            col = corner[0] // TILE_SIZE
            row = corner[1] // TILE_SIZE
            print(col, row)
            print(grid[row][col])
            if (grid[row][col] != TileType.EMPTY):  # 如果角点处是障碍物
                return
        self.x = new_x
        self.y = new_y
        print("\n")
            

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
                    screen.blit(tile_unbreakable_img, (x * TILE_SIZE, y * TILE_SIZE))
                elif self.grid[y][x] == TileType.BREAKABLE:
                    screen.blit(tile_breakable_img, (x * TILE_SIZE, y * TILE_SIZE))

# 主游戏逻辑
def main():
    clock = pygame.time.Clock()
    running = True

    game_map = Map()
    # 初始位置
    player = Player(1, 1)

    while running:
        for y in range(1,GRID_SIZE-1):
            for x in range(1,GRID_SIZE-1):
                screen.blit(background_img, (x * TILE_SIZE, y * TILE_SIZE))
        #screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        # 现在默认中文输入的玩家不需要按shift后才能正常遊玩
        if keyboard.is_pressed('w'):
            player.check_collision(0, -1, game_map.grid)
        if keyboard.is_pressed('s'):    
            player.check_collision(0, 1, game_map.grid)
        if keyboard.is_pressed('a'):
            player.check_collision(-1, 0, game_map.grid)
        if keyboard.is_pressed('d'):
            player.check_collision(1, 0, game_map.grid)

        game_map.draw(screen)
        player.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()