import pygame

class Coin:
    """
    Clase Coin que representa una moneda en el juego.
    Atributos:
    ----------
    rect : pygame.Rect
        Rectángulo que define la posición y tamaño de la moneda.
    image : pygame.Surface
        Imagen de la moneda escalada a 20x20 píxeles.
    Métodos:
    --------
    __init__(x, y):
        Inicializa una instancia de Coin con la posición (x, y).
    draw(screen):
        Dibuja la moneda en la pantalla.
    """
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.image = pygame.image.load("assets/images/coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (20, 20))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)