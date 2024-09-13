
import json
import pygame
from fonts import FontManager


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_manager = FontManager(screen)
        self.font_manager.add_font("title", "./assets/fonts/title_font.ttf", 64)
        self.font_manager.add_font("menu", "./assets/fonts/menu_font.ttf", 32)
        
        self.bg_image = pygame.image.load("./assets/main_menu_bg.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
        
        self.menu_items = ["Play", "Settings", "How to Play", "Quit"]
        self.selected_item = 0
        
        self.high_score = self.load_high_score()
    
    def load_high_score(self):
        try:
            with open("high_score.json", "r") as f:
                data = json.load(f)
                return data.get("high_score", 0)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0
    
    def save_high_score(self, score):
        with open("high_score.json", "w") as f:
            json.dump({"high_score": score}, f)
    
    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        
        # Draw title
        self.font_manager.render_text("Trashy Run", "title", (255, 255, 255), y=50)
        
        # Draw high score
        self.font_manager.render_text(f"High Score: {self.high_score}", "menu", (255, 255, 0), y=130)
        
        # Draw menu items
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 255) if i == self.selected_item else (200, 200, 200)
            self.font_manager.render_text(item, "menu", color, y=250 + i * 60)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                return self.menu_items[self.selected_item].lower().replace(" ", "_")
        return None
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if action := self.handle_event(event):
                    return action

            self.draw()
            pygame.display.flip()

class Settings:
    def __init__(self, screen):
        self.screen = screen
        self.font_manager = FontManager(screen)
        self.font_manager.add_font("title", "./assets/fonts/title_font.ttf", 48)
        self.font_manager.add_font("menu", "./assets/fonts/menu_font.ttf", 32)
        
        self.bg_image = pygame.image.load("./assets/settings_bg.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
        
        self.settings = self.load_settings()
        self.menu_items = ["Music Volume", "SFX Volume", "Back"]
        self.selected_item = 0
    
    def load_settings(self):
        try:
            with open("settings.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"music_volume": 50, "sfx_volume": 50}
    
    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f)
    
    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        
        self.font_manager.render_text("Settings", "title", (255, 255, 255), y=50)
        
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 0) if i == self.selected_item else (255, 255, 255)
            if item == "Back":
                self.font_manager.render_text(item, "menu", color, y=450)
            else:
                self.font_manager.render_text(f"{item}: {self.settings[item.lower().replace(' ', '_')]}", "menu", color, y=200 + i * 60)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_LEFT:
                if self.selected_item < 2:  # Music or SFX volume
                    setting = self.menu_items[self.selected_item].lower().replace(" ", "_")
                    self.settings[setting] = max(0, self.settings[setting] - 10)
            elif event.key == pygame.K_RIGHT:
                if self.selected_item < 2:  # Music or SFX volume
                    setting = self.menu_items[self.selected_item].lower().replace(" ", "_")
                    self.settings[setting] = min(100, self.settings[setting] + 10)
            elif event.key == pygame.K_RETURN:
                if self.selected_item == 2:  # Back
                    return "back"
        return None
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if action := self.handle_event(event):
                    self.save_settings()
                    return action

            self.draw()
            pygame.display.flip()

class HowToPlay:
    def __init__(self, screen):
        self.screen = screen
        self.font_manager = FontManager(screen)
        self.font_manager.add_font("title", "./assets/fonts/title_font.ttf", 48)
        self.font_manager.add_font("text", "./assets/fonts/menu_font.ttf", 24)
        
        self.bg_image = pygame.image.load("./assets/how_to_play_bg.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
        
        self.instructions = [
            "1. Use WASD keys to move your character.",
            "2. Collect trash scattered around the map.",
            "3. Press E to pick up trash when near it.",
            "4. Take the trash to a trash can in one of the corners.",
            "5. Press E near a trash can to dispose of the trash.",
            "6. Each piece of trash disposed increases your score.",
            "7. Try to get the highest score possible!",
            "8. Press ESC to return to the main menu at any time.",
            "",
            "Press any key to return to the main menu."
        ]
    
    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        
        self.font_manager.render_text("How to Play", "title", (255, 255, 255), y=50)
        
        for i, line in enumerate(self.instructions):
            self.font_manager.render_text(line, "text", (255, 255, 255), y=150 + i * 40)
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    return "back"
            
            self.draw()
            pygame.display.flip()

class GameOver:
    def __init__(self, screen, score):
        self.screen = screen
        self.font_manager = FontManager(screen)
        self.font_manager.add_font("title", "./assets/fonts/title_font.ttf", 64)
        self.font_manager.add_font("menu", "./assets/fonts/menu_font.ttf", 32)
        
        self.bg_image = pygame.image.load("./assets/game_over_bg.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (800, 600))
        
        self.score = score
        self.menu_items = ["Replay", "Main Menu"]
        self.selected_item = 0
    
    def draw(self):
        self.screen.blit(self.bg_image, (0, 0))
        
        self.font_manager.render_text("Game Over", "title", (255, 255, 255), y=50)
        self.font_manager.render_text(f"Score: {self.score}", "menu", (255, 255, 0), y=150)
        
        for i, item in enumerate(self.menu_items):
            color = (255, 255, 255) if i == self.selected_item else (200, 200, 200)
            self.font_manager.render_text(item, "menu", color, y=250 + i * 60)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                return self.menu_items[self.selected_item].lower().replace(" ", "_")
        return None
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if action := self.handle_event(event):
                    return action

            self.draw()
            pygame.display.flip()

