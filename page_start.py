import pygame
import sys
from constant import *
from page import Page

class MainMenu(Page):
    def __init__(self, screen):
        super().__init__(screen)
        self.input_boxes = [
            {"rect": pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80, 200, 34), "text": "", "placeholder": "player 1", "active": False},
            {"rect": pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30, 200, 34), "text": "", "placeholder": "player 2", "active": False},
        ]
        self.font = pygame.font.SysFont('Arial', 32)
        self.title_font = pygame.font.SysFont('notosanscjktc', 84)
        self.cursor_pos = [0, 0]  # 每個輸入框的游標位置

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

    def draw_input_boxes(self):
        """繪製輸入框及文字"""
        for i, box in enumerate(self.input_boxes):
            # 繪製輸入框
            pygame.draw.rect(self.screen, WHITE if box["active"] else GRAY, box["rect"], 2)
            
            # 顯示文字或佔位文字
            text_y = box["rect"].y + (box["rect"].height - self.font.get_height()) // 2
            player_text = self.font.render(f"name of {box['placeholder']}:", True, WHITE)
            self.screen.blit(player_text, (box["rect"].x -240, text_y))
            display_text = box["text"] if box["text"] else box["placeholder"]
            text_color = WHITE if box["text"] else GRAY
            text_surface = self.font.render(display_text, True, text_color)
            self.screen.blit(text_surface, (box["rect"].x + 5, text_y))

            # 繪製光標
            if box["active"]:
                cursor_x = self.font.size(box["text"][:self.cursor_pos[i]])[0] + box["rect"].x + 5
                cursor_y = box["rect"].y + (box["rect"].height - self.font.get_height()) // 2
                pygame.draw.line(self.screen, WHITE, (cursor_x, cursor_y), (cursor_x, cursor_y + self.font.get_height()), 2)

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
    
    def start(self):
        """遊戲主界面"""    
        running = True
        clock = pygame.time.Clock()
        while running:
            self.screen.blit(start_img, (0, 0))

            # 繪製標題和提示文字
            title_text = self.title_font.render("Bomberman 轟炸超人", True, WHITE)
            self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
            enter_text = self.font.render("Press ENTER to Start", True, WHITE)
            self.screen.blit(enter_text, (SCREEN_WIDTH // 2 - enter_text.get_width() // 2, SCREEN_HEIGHT // 2 + 200))
            tab_text = self.font.render("Press TAB to Change Input Box", True, WHITE)
            self.screen.blit(tab_text, (SCREEN_WIDTH // 2 - tab_text.get_width() // 2, SCREEN_HEIGHT // 2 + 230))

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
                            return "player 1", "player 2"
                        elif self.input_boxes[0]["text"] == "":
                            return "player 1", self.input_boxes[1]["text"]
                        elif self.input_boxes[1]["text"] == "":
                            return self.input_boxes[0]["text"], "player 2"
                        else:
                            return self.input_boxes[0]["text"], self.input_boxes[1]["text"]
                    else:
                        self.handle_text_input(event)

            # 繪製輸入框
            self.draw_input_boxes()

            pygame.display.flip()
            clock.tick(30)
# if __name__ == "__main__":
#     pygame.init()
#     screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#     mainmenu = MainMenu(screen)
#     mainmenu.start()
#     pygame.quit()
#     sys.exit()