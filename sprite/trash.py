import pygame
from pygame.sprite import Sprite

from sprite.player import Player

class Trash(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, "./game/assests/trash.png")

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def on_collision(self, other):
        if isinstance(other, Player):
            self.x = other.x
            self.y = other.y


class TrashCan(Sprite):
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image: pygame.Surface = pygame.image.load("./game/assets/trashcan.png")

        self.rect: pygame.Rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
    
    def update(self, dt: float) -> None:
        pass

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.rect.x, self.rect.y))

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
