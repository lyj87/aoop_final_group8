import pygame
import sys
from constant import *

class MainMenu:
    def __init__(self):
        self.input_boxes = [
            {"rect": pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80, 200, 34), "text": "", "placeholder": "player1", "active": False},
            {"rect": pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, 200, 34), "text": "", "placeholder": "player2", "active": False},
        ]
        self.cursor_pos = [0, 0]  # 每個輸入框的游標位置
        self.state = "start"

    def handle_text_input(self, event):
        """處理文字輸入事件"""
        for i, box in enumerate(self.input_boxes):
            if box["active"]:
                if event.key == pygame.K_BACKSPACE:
                    if self.cursor_pos[i] > 0:
                        box["text"] = box["text"][:self.cursor_pos[i] - 1] + box["text"][self.cursor_pos[i]:]
                        self.cursor_pos[i] -= 1
                elif event.key == pygame.K_DELETE:
                    if self.cursor_pos[i] < len(box["text"]):
                        box["text"] = box["text"][:self.cursor_pos[i]] + box["text"][self.cursor_pos[i] + 1:]
                elif event.key == pygame.K_LEFT:
                    if self.cursor_pos[i] > 0:
                        self.cursor_pos[i] -= 1
                elif event.key == pygame.K_RIGHT:
                    if self.cursor_pos[i] < len(box["text"]):
                        self.cursor_pos[i] += 1
                else:
                    box["text"] = box["text"][:self.cursor_pos[i]] + event.unicode + box["text"][self.cursor_pos[i]:]
                    self.cursor_pos[i] += 1

    def draw_input_boxes(self, screen, font):
        """繪製輸入框及文字"""
        for i, box in enumerate(self.input_boxes):
            # 繪製輸入框
            pygame.draw.rect(screen, WHITE if box["active"] else GRAY, box["rect"], 2)
            
            # 顯示文字或佔位文字
            text_y = box["rect"].y + (box["rect"].height - font.get_height()) // 2
            player_text = font.render(f"name of {box['placeholder']}:", True, WHITE)
            screen.blit(player_text, (box["rect"].x -240, text_y))
            display_text = box["text"] if box["text"] else box["placeholder"]
            text_color = WHITE if box["text"] else GRAY
            text_surface = font.render(display_text, True, text_color)
            screen.blit(text_surface, (box["rect"].x + 5, text_y))

            # 繪製光標
            if box["active"]:
                cursor_x = font.size(box["text"][:self.cursor_pos[i]])[0] + box["rect"].x + 5
                cursor_y = box["rect"].y + (box["rect"].height - font.get_height()) // 2
                pygame.draw.line(screen, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + font.get_height()), 2)

    def handle_mouse_click(self, event):
        """處理鼠標點擊事件"""
        for i, box in enumerate(self.input_boxes):
            if box["rect"].collidepoint(event.pos):
                box["active"] = True
            else:
                box["active"] = False

    def handle_tab_press(self):
        """處理 Tab 鍵切換輸入框"""
        active_index = next((i for i, box in enumerate(self.input_boxes) if box["active"]), -1)
        next_index = (active_index + 1) % len(self.input_boxes) if active_index != -1 else 0
        for i, box in enumerate(self.input_boxes):
            box["active"] = (i == next_index)

    def handle_up_down_press(self, event):
        """處理上下鍵切換輸入框"""
        active_index = next((i for i, box in enumerate(self.input_boxes) if box["active"]), -1)
        if event.key == pygame.K_UP:
            next_index = 0
        elif event.key == pygame.K_DOWN:
            next_index = 1
        for i, box in enumerate(self.input_boxes):
            box["active"] = (i == next_index)
    
    def start(self, screen, font, title_font):
        """遊戲主界面"""    
        running = True
        clock = pygame.time.Clock()
        while running:
            screen.blit(start_img, (0, 0))

            # 繪製標題和提示文字
            title_text = title_font.render("Bomberman 轟炸超人", True, WHITE)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
            enter_text = font.render("Press ENTER to Start", True, WHITE)
            screen.blit(enter_text, (SCREEN_WIDTH // 2 - enter_text.get_width() // 2, SCREEN_HEIGHT // 2 + 200))
            tab_text = font.render("Press TAB to Change Input Box", True, WHITE)
            screen.blit(tab_text, (SCREEN_WIDTH // 2 - tab_text.get_width() // 2, SCREEN_HEIGHT // 2 + 230))

            # 處理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse_click(event)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.handle_tab_press()
                    elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                        self.handle_up_down_press(event)
                    elif event.key == pygame.K_RETURN:
                        self.state = "game"
                        if self.input_boxes[0]["text"] == "" and self.input_boxes[1]["text"] == "":
                            return "player1", "player2"
                        elif self.input_boxes[0]["text"] == "":
                            return "player1", self.input_boxes[1]["text"]
                        elif self.input_boxes[1]["text"] == "":
                            return self.input_boxes[0]["text"], "player2"
                        else:
                            return self.input_boxes[0]["text"], self.input_boxes[1]["text"]
                    else:
                        self.handle_text_input(event)

            # 繪製輸入框
            self.draw_input_boxes(screen, font)

            pygame.display.flip()
            clock.tick(30)


# 運行程式
if __name__ == "__main__":
    pygame.init()
    font = pygame.font.SysFont('Arial', 32)
    title_font = pygame.font.SysFont('notosanscjktc', 84)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    mainmenu = MainMenu()
    names = mainmenu.start(screen, font, title_font)
    print('player1:',names[0], ', player2:',names[1])