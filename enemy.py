import pygame
import random

class Enemy:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 70, 70)
        self.image = pygame.image.load("assets/images/character/enemy/enemy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.health = 1
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        if self.rect.right > 1280 or self.rect.left < 0:
            self.speed = -self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.die()

    def die(self):
        self.rect.x = -100

class FinalBoss(Enemy):
    """
    Clase FinalBoss que hereda de Enemy y representa al jefe final en el juego.
    Métodos:
    --------
    __init__(x, y):
        Inicializa el jefe final con su posición, imagen, salud y otros atributos.
    update():
        Actualiza la posición del jefe final y maneja el ataque de bolas de poder.
    fire_power_ball():
        Crea y lanza una nueva bola de poder desde la posición del jefe final.
    draw(screen):
        Dibuja al jefe final y sus bolas de poder en la pantalla.
    draw_health_bar(screen):
        Dibuja la barra de salud del jefe final en la pantalla.
    take_damage(damage):
        Reduce la salud del jefe final en función del daño recibido y verifica si debe morir.
    die():
        Maneja la lógica cuando el jefe final muere.
    increase_attack_delay():
        Aumenta el tiempo de retraso entre los ataques del jefe final.
    """
    def __init__(self, x, y):
        super().__init__(x, y, speed=3)
        self.rect = pygame.Rect(x, y, 150, 150)
        self.image = pygame.image.load("assets/images/character/enemy/boss_2.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.health = 20
        self.power_balls = []
        self.attack_delay = 60

    def update(self):
        self.rect.y += self.speed
        if self.rect.top < 0 or self.rect.bottom > 720:
            self.speed = -self.speed
        self.attack_delay -= 1
        if self.attack_delay <= 0:
            self.fire_power_ball()
            self.attack_delay = 60

    def fire_power_ball(self):
        new_ball = PlayerPowerBall(self.rect.centerx, self.rect.centery, speed=-10)
        self.power_balls.append(new_ball)

    def draw(self, screen):
        super().draw(screen)
        for ball in self.power_balls:
            ball.update()
            ball.draw(screen)

    def draw_health_bar(self, screen):
        bar_width = 150
        bar_height = 10
        fill = (self.health / 20) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y - 20, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y - 20, fill, bar_height)
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), outline_rect, 2)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.rect.x = -100

    def increase_attack_delay(self):
        self.attack_delay += 10

class PlayerPowerBall:
    def __init__(self, x, y, speed=10):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = speed
        self.image = pygame.image.load("assets/images/character/player/magic1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))

    def update(self):
        self.rect.x += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
