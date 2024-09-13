from typing import List

import pygame
import random

from pygame.sprite import Sprite
from sprite.table import DirtyTable
from .trash import Trash

class NPC(Sprite):
    def __init__(self, x: int, y: int, map_width: int, map_height: int):
        super().__init__()
        self.original_image: pygame.Surface = pygame.image.load("./assets/npc.png")
        self.image: pygame.Surface = self.original_image
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed: int = 2
        self.direction: str = 'down'
        self.map_width: int = map_width
        self.map_height: int = map_height
        
        self.movement_timer: float = 0
        self.movement_interval: float = 2.0  # Change direction every 2 seconds
        
        self.throw_timer: float = 0
        self.throw_interval: float = 8.0  # Throw trash every 8 seconds

    def update(self, dt: float, all_sprites: pygame.sprite.Group, trash_group: pygame.sprite.Group) -> None:
        self.movement_timer += dt
        self.throw_timer += dt
        
        if self.movement_timer >= self.movement_interval:
            self.change_direction()
            self.movement_timer = 0
        
        if self.throw_timer >= self.throw_interval:
            self.throw_trash(all_sprites, trash_group)
            self.throw_timer = 0
        
        self.move(dt)

    def change_direction(self) -> None:
        self.direction = random.choice(['up', 'down', 'left', 'right'])
        self.update_image()

    def move(self, dt: float) -> None:
        new_x, new_y = self.rect.x, self.rect.y
        
        if self.direction == 'up':
            new_y -= self.speed
        elif self.direction == 'down':
            new_y += self.speed
        elif self.direction == 'left':
            new_x -= self.speed
        elif self.direction == 'right':
            new_x += self.speed
        
        # Check boundaries
        new_x = max(0, min(new_x, self.map_width - self.rect.width))
        new_y = max(0, min(new_y, self.map_height - self.rect.height))
        
        self.rect.x, self.rect.y = new_x, new_y

    def update_image(self) -> None:
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.original_image, True, False)
        elif self.direction == 'right':
            self.image = self.original_image
        elif self.direction == 'up':
            self.image = pygame.transform.rotate(self.original_image, 90)
        elif self.direction == 'down':
            self.image = pygame.transform.rotate(self.original_image, -90)

    def throw_trash(self, all_sprites: pygame.sprite.Group, trash_group: pygame.sprite.Group, tables: List[DirtyTable]) -> None:
        if nearby_tables := [
            table for table in tables if self.rect.colliderect(table.rect)
        ]:
            target_table = random.choice(nearby_tables)
            target_table.make_dirty(all_sprites, trash_group)
        else:
            # If no tables nearby, throw trash on the ground as before
            trash_x = self.rect.x + random.randint(-50, 50)
            trash_y = self.rect.y + random.randint(-50, 50)

            # Ensure trash is within map boundaries
            trash_x = max(0, min(trash_x, self.map_width - 32))
            trash_y = max(0, min(trash_y, self.map_height - 32))

            new_trash = Trash(trash_x, trash_y)
            all_sprites.add(new_trash)
            trash_group.add(new_trash)

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def on_collision(self, other: Sprite) -> None:
        # Handle collisions if necessary
        pass