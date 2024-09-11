import pygame

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
