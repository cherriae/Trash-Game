from __future__ import annotations

import pygame
import random

from misc import HowToPlay, MainMenu, Settings
from sprite.trash import EatenFood, TrashBag, WaterSpill

from .sprite import Camera, Player, TrashCan


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Trashy Run")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "main_menu"

        # Create screens
        self.main_menu = MainMenu(self.screen)
        self.settings = Settings(self.screen)
        self.how_to_play = HowToPlay(self.screen)

        # Load and scale background
        self.background = pygame.image.load("./assets/background.png")
        self.background = pygame.transform.scale(self.background, (2000, 2000))
        
        # Create camera
        self.camera = Camera(800, 600, 2000, 2000)

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.trash_group = pygame.sprite.Group()
        self.trashcan_group = pygame.sprite.Group()

        # Create player
        self.player = Player(400, 300, self.screen, 2000, 2000)
        self.all_sprites.add(self.player)

        # Create mini-map surface
        self.minimap_size = (150, 150)
        self.minimap_surf = pygame.Surface(self.minimap_size)

        # Load and scale player image for mini-map
        self.minimap_player_image = pygame.image.load("./assets/player_icon.png")
        self.minimap_player_image = pygame.transform.scale(self.minimap_player_image, (10, 10))

        self.create_trash(20)
        self.create_trashcans()

    def create_trash(self, count):
        trash_types = [WaterSpill, EatenFood, TrashBag]
        for _ in range(count):
            x = random.randint(0, 1900)
            y = random.randint(0, 1900)
            trash = random.choice(trash_types)(x, y)
            self.all_sprites.add(trash)
            self.trash_group.add(trash)

    def create_trashcans(self):
        corners = [(0, 0), (1900, 0), (0, 1900), (1900, 1900)]  # Adjust based on your map size
        for corner in corners:
            trashcan = TrashCan(corner[0], corner[1])
            self.all_sprites.add(trashcan)
            self.trashcan_group.add(trashcan)

    def run(self):
        while self.running:
            if self.state == "main_menu":
                action = self.main_menu.run()
                if action == "play":
                    self.state = "game"
                elif action == "settings":
                    self.state = "settings"
                elif action == "how_to_play":
                    self.state = "how_to_play"
                elif action == "quit":
                    self.running = False
            elif self.state == "settings":
                action = self.settings.run()
                if action == "back" or action == "quit":
                    self.state = "main_menu"
            elif self.state == "how_to_play":
                action = self.how_to_play.run()
                if action == "back" or action == "quit":
                    self.state = "main_menu"
            elif self.state == "game":
                self.run_game()

        pygame.quit()

    def run_game(self):
        dt = self.clock.tick(60) / 1000.0
        self.handle_events()
        self.update(dt)
        self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.player.drop_trash(self.trashcan_group)
                elif event.key == pygame.K_ESCAPE:
                    self.state = "main_menu"

    def update(self, dt):
        old_pos = self.player.rect.copy()
        self.all_sprites.update(dt)

        collided_trashcans = pygame.sprite.spritecollide(self.player, self.trashcan_group, False)
        for trashcan in collided_trashcans:
            self.handle_collision(self.player, trashcan, old_pos)
            self.player.on_collision(trashcan)

        collided_trash = pygame.sprite.spritecollide(self.player, self.trash_group, False)
        for trash in collided_trash:
            self.player.on_collision(trash)

        self.camera.update(self.player)

        # Update high score
        if self.player.score > self.main_menu.high_score:
            self.main_menu.high_score = self.player.score
            self.main_menu.save_high_score(self.player.score)

    def handle_collision(self, player, obstacle, old_pos):
        # Calculate the overlap on each side
        left_overlap = player.rect.right - obstacle.rect.left
        right_overlap = obstacle.rect.right - player.rect.left
        top_overlap = player.rect.bottom - obstacle.rect.top
        bottom_overlap = obstacle.rect.bottom - player.rect.top

        # Find the side with the smallest overlap
        min_overlap = min(left_overlap, right_overlap, top_overlap, bottom_overlap)

        # Push the player back based on the smallest overlap
        if min_overlap == left_overlap:
            player.rect.right = obstacle.rect.left
        elif min_overlap == right_overlap:
            player.rect.left = obstacle.rect.right
        elif min_overlap == top_overlap:
            player.rect.bottom = obstacle.rect.top
        elif min_overlap == bottom_overlap:
            player.rect.top = obstacle.rect.bottom

    def draw_minimap(self):
        # Clear mini-map surface
        self.minimap_surf.fill((200, 200, 200))  # Light gray background

        # Calculate scale factors
        scale_x = self.minimap_size[0] / 2000
        scale_y = self.minimap_size[1] / 2000

        # Draw player on mini-map
        mini_player_pos = (int(self.player.rect.x * scale_x), int(self.player.rect.y * scale_y))
        mini_player_rect = self.minimap_player_image.get_rect(center=mini_player_pos)
        self.minimap_surf.blit(self.minimap_player_image, mini_player_rect)

        # Draw other entities on mini-map (if any)
        for sprite in self.all_sprites:
            if sprite != self.player:
                mini_sprite_pos = (int(sprite.rect.x * scale_x), int(sprite.rect.y * scale_y))
                pygame.draw.circle(self.minimap_surf, (0, 255, 0), mini_sprite_pos, 2)

        # Draw mini-map on main screen
        minimap_pos = (10, self.screen.get_height() - self.minimap_size[1] - 10)
        self.screen.blit(self.minimap_surf, minimap_pos)
        pygame.draw.rect(self.screen, (0, 0, 0), (*minimap_pos, *self.minimap_size), 2)

    def draw(self):
        # Draw background
        self.screen.blit(self.background, self.camera.apply(self.background.get_rect()))

        # Draw sprites
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # Draw mini-map
        self.draw_minimap()

        pygame.display.flip()

    def draw(self):
        self.screen.blit(self.background, self.camera.apply(self.background.get_rect()))

        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        self.draw_minimap()

        # Draw score
        self.player.fonts.render_text(f"Score: {self.player.score}", "default", (255, 255, 255), x=10, y=10)

        pygame.display.flip()
        
Game().run()