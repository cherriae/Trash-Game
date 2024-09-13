import pygame
from pygame.sprite import Sprite
from sprite.player import Player


class Trash(Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()
        self.image: pygame.Surface = pygame.image.load(image_path)
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def on_collision(self, other):
        pass  # Handle collision logic in Player class


class WaterSpill(Trash):
    def __init__(self, x, y):
        super().__init__(x, y, "./game/assets/water_spill.png")


class EatenFood(Trash):
    def __init__(self, x, y):
        super().__init__(x, y, "./game/assets/eaten_food.png")


class TrashBag(Trash):
    def __init__(self, x, y):
        super().__init__(x, y, "./game/assets/trash_bag.png")


class TrashCan(Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image: pygame.Surface = pygame.image.load("./game/assets/trashcan.png")
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect.topleft)

    def on_collision(self, other: Sprite) -> None:
        if isinstance(other, Player):
            # Prevent the player from moving through the trash can
            if self.rect.colliderect(other.rect):
                # Adjust the player's position based on collision direction
                if other.rect.right > self.rect.left and other.rect.left < self.rect.left:
                    other.rect.right = self.rect.left  # Stop player moving right

                elif other.rect.left < self.rect.right and other.rect.right > self.rect.right:
                    other.rect.left = self.rect.right  # Stop player moving left

                elif other.rect.bottom > self.rect.top and other.rect.top < self.rect.top:
                    other.rect.bottom = self.rect.top  # Stop player moving down

                elif other.rect.top < self.rect.bottom and other.rect.bottom > self.rect.bottom:
                    other.rect.top = self.rect.bottom  # Stop player moving up


class Dumpster(Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.image: pygame.Surface = pygame.image.load("./game/assets/dumpster.png")
        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect.topleft)

    def on_collision(self, other: Sprite) -> None:
        if isinstance(other, Player):
            # Prevent the player from moving through the trash can
            if self.rect.colliderect(other.rect):
                # Adjust the player's position based on collision direction
                if other.rect.right > self.rect.left and other.rect.left < self.rect.left:
                    other.rect.right = self.rect.left  # Stop player moving right

                elif other.rect.left < self.rect.right and other.rect.right > self.rect.right:
                    other.rect.left = self.rect.right  # Stop player moving left

                elif other.rect.bottom > self.rect.top and other.rect.top < self.rect.top:
                    other.rect.bottom = self.rect.top  # Stop player moving down

                elif other.rect.top < self.rect.bottom and other.rect.bottom > self.rect.bottom:
                    other.rect.top = self.rect.bottom  # Stop player moving up