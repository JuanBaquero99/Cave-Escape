import pygame

class Background:
    def __init__(self):
        self.layers = [
            [self.load_background("assets/images/background/parallax-mountain-bg.png"), 0.5, 0],
            [self.load_background("assets/images/background/parallax-mountain-mountains.png"), 1.0, 0],
            [self.load_background("assets/images/background/parallax-mountain-montain-far.png"), 1.5, 0],
            [self.load_background("assets/images/background/parallax-mountain-trees.png"), 2.0, 0],
            [self.load_background("assets/images/background/parallax-mountain-foreground-trees.png"), 2.5, 0]
        ]

    def load_background(self, filename):
        background = pygame.image.load(filename).convert_alpha()
        background = pygame.transform.scale(background, (1280, 720))
        return background

    def update(self, shift):
        for layer in self.layers:
            layer[2] += shift * layer[1]
            if layer[2] <= -1280:
                layer[2] += 1280
            elif layer[2] >= 1280:
                layer[2] -= 1280

    def draw(self, screen):
        for layer in self.layers:
            screen.blit(layer[0], (layer[2], 0))
            if layer[2] < 0:
                screen.blit(layer[0], (layer[2] + 1280, 0))
            elif layer[2] > 0:
                screen.blit(layer[0], (layer[2] - 1280, 0))