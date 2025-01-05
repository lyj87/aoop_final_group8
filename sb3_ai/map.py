import numpy as np

def generate_map(size=13):
    game_map = np.zeros((size, size), dtype=int)
    game_map[0, :] = 1
    game_map[-1, :] = 1
    game_map[:, 0] = 1
    game_map[:, -1] = 1

    for i in range(2, size - 1, 2):
        for j in range(2, size - 1, 2):
            game_map[i, j] = 1

    np.random.seed(42)
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            if game_map[i, j] == 0 and (i > 2 or j > 2):
                if np.random.rand() < 0.3:
                    game_map[i, j] = 2

    return game_map