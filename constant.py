# 常量定义
TILE_SIZE = 32  # 图片大小
GRID_SIZE = 21  # 地图大小
SCOREBOARD_WIDTH = 200  # 计分板宽度
SCREEN_WIDTH = GRID_SIZE * TILE_SIZE + SCOREBOARD_WIDTH
SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 石块类型
class TileType:
    UNBREAKABLE = 0
    BREAKABLE = 1
    EMPTY = 2
    AROUND = 3
    BUFF_RANGE = 4
    BUFF_NUM = 5
    HEAL = 6