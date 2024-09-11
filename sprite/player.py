from __future__ import annotations

import pygame
from pygame.sprite import Sprite
from ..fonts import FontManager
from .trash import Trash, TrashCan


class Camera:
    def __init__(self, width: int, height: int, map_width: int, map_height: int) -> None:
        self.camera: pygame.Rect = pygame.Rect(0, 0, width, height)

        self.width: int = width
        self.height: int = height

        self.map_width: int = map_width
        self.map_height: int = map_height

    def apply(self, entity: Sprite) -> pygame.Rect:
        return entity.rect.move(self.camera.topleft)

    def update(self, target: Sprite) -> None:
        x: int = -target.rect.centerx + int(self.width / 2)
        y: int = -target.rect.centery + int(self.height / 2)

        # Limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top

        x = max(-(self.map_width - self.width), x)  # right
        y = max(-(self.map_height - self.height), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)


class Player(Sprite):
    def __init__(self, x: int, y: int, screen: pygame.Surface, map_width: int, map_height: int) -> None:
        super().__init__()
        self.original_image: pygame.Surface = pygame.image.load("./assests/player.png")
        self.image: pygame.Surface = self.original_image

        self.rect: pygame.Rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.score: int = 0
        self.speed: int = 5
        self.holding_trash: Trash = None
        self._has_trash: bool = False
        
        self.screen: pygame.Surface = screen
        self.fonts: FontManager = FontManager(self.screen)
        
        self.map_width: int = map_width
        self.map_height: int = map_height
        self.direction: str = 'down'  # track facing direction
   
    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        new_x, new_y = self.rect.x, self.rect.y
        moved = False

        if keys[pygame.K_w]:
            new_y -= self.speed
            self.direction = 'up'
            moved = True

        if keys[pygame.K_s]:
            new_y += self.speed
            self.direction = 'down'
            moved = True

        if keys[pygame.K_a]:
            new_x -= self.speed
            self.direction = 'left'
            moved = True

        if keys[pygame.K_d]:
            new_x += self.speed
            self.direction = 'right'
            moved = True

        # Check boundaries
        new_x = max(0, min(new_x, self.map_width - self.rect.width))
        new_y = max(0, min(new_y, self.map_height - self.rect.height))

        self.rect.x, self.rect.y = new_x, new_y

        # Update the player's image based on direction
        if moved:
            self.update_image()

    def update_image(self):
        if self.direction == 'left':
            self.image = pygame.transform.flip(self.original_image, True, False)

        elif self.direction == 'right':
            self.image = self.original_image

        elif self.direction == 'up':
            self.image = pygame.transform.rotate(self.original_image, 90)

        elif self.direction == 'down':
            self.image = pygame.transform.rotate(self.original_image, -90)

    def draw(self, screen: pygame.Surface) -> None:
        # Draw the player
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def pickup_trash(self, trash: Trash) -> None:
        if not self._has_trash:
            self._has_trash = True
            self.holding_trash = trash

            self.holding_trash.rect.x = self.rect.x
            self.holding_trash.rect.y = self.rect.y

            self.fonts.render_text("You picked up the trash.", "default", (255, 255, 255))

    def drop_trash(self) -> None:
        if self._has_trash:
            self._has_trash = False

            self.holding_trash.rect.x = self.rect.x
            self.holding_trash.rect.y = self.rect.y + 1
            
            self.holding_trash = None
            self.fonts.render_text("You have dropped the trash on the ground.", "default", (255, 255, 255))

    def drop_trash_in_can(self, trashcan: TrashCan) -> None:
        if not self._has_trash:
            self.fonts.render_text("You need trash to drop it in the trash can.", "default", (255, 255, 255))
            return

        # Check if player is close enough to the trash can
        if pygame.sprite.collide_rect(self, trashcan):
            self._has_trash = False
            if self.holding_trash:
                self.holding_trash.kill()  # Remove trash from all sprite groups

            self.holding_trash = None
            self.score += 1

            self.fonts.render_text("You dropped the trash in the trash can.", "default", (255, 255, 255))
        else:
            self.fonts.render_text("Move closer to the trash can.", "default", (255, 255, 255))


    def on_collision(self, other: Sprite) -> None:
        if isinstance(other, Trash):
            if pygame.key.get_pressed()[pygame.K_e]:
                if not self._has_trash:
                    self.pickup_trash(other)
                else:
                    self.drop_trash()

        elif isinstance(other, TrashCan):
            if pygame.key.get_pressed()[pygame.K_e]:
                self.drop_trash_in_can(other)
