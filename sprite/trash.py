import pygame
from pygame.sprite import Sprite

from sprite.player import Player

class TrashType(Sprite):
    def __init__(self, x: int, y: int, image_path: str, score: int):
        super().__init__()
        self.image: pygame.Surface = pygame.image.load(image_path)
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.score = score

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

class WaterSpill(TrashType):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "./assets/water_spill.png", 1)

class EatenFood(TrashType):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "./assets/eaten_food.png", 1)

class TrashBag(TrashType):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, "./assets/trash_bag.png", 2)

class Mop(Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image: pygame.Surface = pygame.image.load("./assets/mop.png")
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

class MopStation(Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image: pygame.Surface = pygame.image.load("./assets/mop_station.png")
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def on_collision(self, other: Sprite) -> None:
        if isinstance(other, Player) and self.rect.colliderect(other.rect):
            if other.rect.right > self.rect.left and other.rect.left < self.rect.left:
                other.rect.right = self.rect.left  # Stop player moving right
        
            elif other.rect.left < self.rect.right and other.rect.right > self.rect.right:
                other.rect.left = self.rect.right  # Stop player moving left
        
            elif other.rect.bottom > self.rect.top and other.rect.top < self.rect.top:
                other.rect.bottom = self.rect.top  # Stop player moving down
        
            elif other.rect.top < self.rect.bottom and other.rect.bottom > self.rect.bottom:
                other.rect.top = self.rect.bottom  # Stop player moving up


class Trashcan(Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image: pygame.Surface = pygame.image.load("./assets/trashcan.png")
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)
    
    def on_collision(self, other: Sprite) -> None:
        if isinstance(other, Player) and self.rect.colliderect(other.rect):
            if other.rect.right > self.rect.left and other.rect.left < self.rect.left:
                other.rect.right = self.rect.left  # Stop player moving right
        
            elif other.rect.left < self.rect.right and other.rect.right > self.rect.right:
                other.rect.left = self.rect.right  # Stop player moving left
        
            elif other.rect.bottom > self.rect.top and other.rect.top < self.rect.top:
                other.rect.bottom = self.rect.top  # Stop player moving down
        
            elif other.rect.top < self.rect.bottom and other.rect.bottom > self.rect.bottom:
                other.rect.top = self.rect.bottom  # Stop player moving up


class Dumpster(Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()
        self.image: pygame.Surface = pygame.image.load("./assets/dumpster.png")
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def on_collision(self, other: Sprite) -> None:
        if isinstance(other, Player) and self.rect.colliderect(other.rect):
            if other.rect.right > self.rect.left and other.rect.left < self.rect.left:
                other.rect.right = self.rect.left  # Stop player moving right
        
            elif other.rect.left < self.rect.right and other.rect.right > self.rect.right:
                other.rect.left = self.rect.right  # Stop player moving left
        
            elif other.rect.bottom > self.rect.top and other.rect.top < self.rect.top:
                other.rect.bottom = self.rect.top  # Stop player moving down
        
            elif other.rect.top < self.rect.bottom and other.rect.bottom > self.rect.bottom:
                other.rect.top = self.rect.bottom  # Stop player moving up
