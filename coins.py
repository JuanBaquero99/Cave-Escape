import pygame

class Coin:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.image = pygame.image.load("assets/images/coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)