import random
import pygame
from .trash import Trash

# Cafeteria table
class Table(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image: pygame.Surface = pygame.image.load("./game/assets/table.png")

        self.rect: pygame.Rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
    
    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.rect.x, self.rect.y))
    
    def on_collision(self, other: pygame.sprite.Sprite) -> None:
        pass

class DirtyTable(Table):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.dirty_image: pygame.Surface = pygame.image.load("./game/assets/dirty_table.png")
        self.is_dirty: bool = False
        self.trash: Trash = None

    def make_dirty(self, all_sprites: pygame.sprite.Group, trash_group: pygame.sprite.Group) -> None:
        if not self.is_dirty:
            self.is_dirty = True
            self.image = self.dirty_image
            
            # Create trash on the table
            trash_x = self.rect.x + random.randint(10, self.rect.width - 10)
            trash_y = self.rect.y + random.randint(10, self.rect.height - 10)
            self.trash = Trash(trash_x, trash_y)
            all_sprites.add(self.trash)
            trash_group.add(self.trash)

    def clean(self, all_sprites: pygame.sprite.Group, trash_group: pygame.sprite.Group) -> None:
        if self.is_dirty:
            self.is_dirty = False
            self.image = pygame.image.load("./game/assets/table.png")
            if self.trash:
                all_sprites.remove(self.trash)
                trash_group.remove(self.trash)
                self.trash = None

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)
        if self.trash:
            self.trash.draw(screen)
