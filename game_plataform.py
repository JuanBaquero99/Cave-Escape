import pygame
import random

class Platform:
    def __init__(self, x, y, width, height, tile_images):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(random.choice(tile_images)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)