from __future__ import annotations

import pygame
import random
from .sprite import Camera, Player, Trash, TrashCan

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True

        # Load and scale background
        self.background = pygame.image.load("./assests/background.png")
        self.background = pygame.transform.scale(self.background, (2000, 2000))
        
        # Create camera
        self.camera = Camera(2000, 2000)

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()

        # Create player
        self.player = Player(400, 300)
        self.all_sprites.add(self.player)

        # Create mini-map surface
        self.minimap_size = (150, 150)
        self.minimap_surf = pygame.Surface(self.minimap_size)

        # Load and scale player image for mini-map
        self.minimap_player_image = pygame.image.load("./assests/player_icon.png")
        self.minimap_player_image = pygame.transform.scale(self.minimap_player_image, (10, 10))

    def create_trash(self, count):
        for _ in range(count):
            x = random.randint(0, 1900)  # Adjust based on your map size
            y = random.randint(0, 1900)
            trash = Trash(x, y)
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
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.player.drop_trash(self.trashcan_group)

    def update(self, dt):
        # Store the player's previous position
        old_pos = self.player.rect.copy()

        # Update all sprites
        self.all_sprites.update(dt)

        # Check for collisions between player and trash cans
        collided_trashcans = pygame.sprite.spritecollide(self.player, self.trashcan_group, False)
        for trashcan in collided_trashcans:
            self.handle_collision(self.player, trashcan, old_pos)
            self.player.on_collision(trashcan)

        # Check for collisions between player and trash
        collided_trash = pygame.sprite.spritecollide(self.player, self.trash_group, False)
        for trash in collided_trash:
            self.player.on_collision(trash)

        self.camera.update(self.player)

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
